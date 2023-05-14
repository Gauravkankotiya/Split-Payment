from django.contrib.auth import authenticate
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from .models import Expenses, Group
from django.db.models import Sum, F


@api_view(["POST"])
def login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        # print("----------------------------->",username)
        password = request.POST.get("password")
        user = authenticate(username=username, password=password)
        # print(user)
        if user is not None:
            auth_user = User.objects.get(id=user.id)
            request.session["id"] = auth_user.id
            groups = Group.objects.filter(users__icontains=auth_user.id).values(
                "id", "name"
            )
            res = {"status": 1, "message": "Login Successfull!", "groups": groups}
            return Response(res)
        else:
            res = {"status": 1, "message": "Invalid Credential"}
            return Response(res)


@api_view(["POST"])
def register(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        try:
            User.objects.get(username=username)
            res = {"status": 1, "message": "User Already Exists with that user name!!!"}
            return Response(res)
        except:
            try:
                user = User()
                user.username = username
                user.email = email
                user.set_password(password)
                user.save()
                # print("**********************1")
                auth_user = User.objects.get(username=username)
                # print("******************************22")
                res = {
                    "status": 0,
                    "message": "Successfully Register",
                }

                request.session["id"] = auth_user.id
                return Response(res)

            except Exception as e:
                # print(e)
                res = {
                    "status": 1,
                    "message": "Internal Error",
                }
                return Response(res)


@api_view(["POST"])
def all_users(request):
    if request.method == "POST":
        try:
            # print("*****************************>")
            # print(request.session['id'])
            User.objects.get(id=request.session["id"])
            try:
                users = User.objects.all().values("id", "username")
                res = {"status": 0, "users": users}
                return Response(res)
            except Exception as e:
                # print(e)
                res = {"status": 1, "message": "Internal Error"}
                return Response(res)
        except Exception as e:
            # print(e)
            res = {"status": 1, "message": "Access Denied"}
            return Response(res)


@api_view(["POST"])
def make_group(request):
    if request.method == "POST":
        try:
            user_self = request.session["id"]
            creator = User.objects.get(id=user_self)
            name = request.POST.get("group_name")
            users = request.POST.get("users")
            users = users + f",{user_self}"
            g = Group()
            g.name = name
            g.created_by = creator
            g.users = users
            g.save()
            group = Group.objects.last()
            user_list = users.split(",")
            for user in user_list:
                u = User.objects.get(id=user)
                ex = Expenses()
                ex.user = u
                ex.group_name = group
                ex.payment = 0
                ex.save()

            res = {
                "status": 0,
                "message": "Group Successfully Created!!!",
                "gid": group.id,
                "group_name": group.name,
            }
            return Response(res)
        except Exception as e:
            # print(e)
            res = {"status": 1, "message": "Internal Error"}
            return Response(res)


@api_view(["POST"])
def add_expenses(request):
    if request.method == "POST":
        try:
            user = User.objects.get(id=request.session["id"])
            group = request.POST.get("group")
            payment = request.POST.get("payment")
            msg = request.POST.get("message")
            group = Group.objects.get(id=group)
            # print("------------------------>",user.username)
            ex = Expenses()
            ex.user = user
            ex.payment = payment
            ex.group_name = group
            ex.msg = msg
            ex.save()

            res = {
                "status": 0,
                "message": "Expenses Succesfully added",
                "user": user.username,
                "payment": payment,
                "msg": msg,
                "group": group.id,
            }
            return Response(res)

        except Exception as e:
            # print(e)
            res = {"status": 1, "message": "Access Denied!!!"}
            return Response(res)


@api_view(["POST"])
def caluculate(request):
    if request.method == "POST":
        try:
            User.objects.get(id=request.session["id"])
            group = request.POST.get("group")
            # print("----------->",group)
            group = Group.objects.get(id=group)
            users = (
                Expenses.objects.filter(group_name=group)
                .values("user__username")
                .annotate(payment=Sum("payment"), user_name=F("user__username"))
                .values("user_name", "payment")
            )
            # print("***************************************" ,len(users))
            # print(users)
            total = 0
            for user in users:
                total = total + user["payment"]

            per_person = total / len(users)
            group.total = total
            group.per_person = per_person
            group.save()
            # print("--------------Total : ",total)
            # print("--------------Per Person : ",per_person)
            for u in users:
                u["payment"] = u["payment"] - per_person
            final_list = []
            # print(users)
            sortedRem = sorted(users, key=lambda p: p["payment"], reverse=True)
            for i in range(len(sortedRem) - 1, -1, -1):
                if sortedRem[i]["payment"] < 0:
                    for j in range(len(sortedRem)):
                        if sortedRem[j]["payment"] > 0:
                            ANS = sortedRem[j]["payment"] + sortedRem[i]["payment"]
                            if ANS < 0:
                                final_list.append(
                                    sortedRem[i]["user_name"]
                                    + " needs to give "
                                    + str(sortedRem[j]["payment"])
                                    + " to the "
                                    + sortedRem[j]["user_name"]
                                )
                                sortedRem[j]["payment"] = 0
                                sortedRem[i]["payment"] = ANS
                            elif ANS > 0:
                                final_list.append(
                                    sortedRem[i]["user_name"]
                                    + " needs to give "
                                    + str(abs(sortedRem[i]["payment"]))
                                    + " to the "
                                    + sortedRem[j]["user_name"]
                                )
                                sortedRem[j]["payment"] = ANS
                                sortedRem[i]["payment"] = 0
                                j = len(sortedRem)
                            else:
                                final_list.append(
                                    sortedRem[i]["user_name"]
                                    + " needs to give "
                                    + str(sortedRem[j]["payment"])
                                    + " to the "
                                    + sortedRem[j]["user_name"]
                                )
                                sortedRem[j]["payment"] = 0
                                sortedRem[i]["payment"] = 0
                                j = len(sortedRem)

            return Response({"status": 0, "final_ans": final_list})
        except:
            res = {"status": 1, "message": "Access Denied!!!"}
            return Response(res)
