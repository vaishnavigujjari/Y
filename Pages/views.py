from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
import pymysql
from Pages.models import country_team,match_user,user_team,choosen_players,user,match_performance
from django.views.decorators.csrf import csrf_exempt
#import json


points =100
admin_match_id=0
master_user_id=0
master_match_id=0
sel_players_user=[]

def Home(request):
    el=list(user.objects.values('email'))
    elist=[]
    for i in el:
        elist.append(i['email'])
    print(elist)
    return render(request,'dummy.html',{'hello':elist})
def logout(request):
    global master_user_id
    master_user_id=0
    print(master_user_id)
    return render(request,'login.html')
def login(request):
    global master_user_id
    if request.method=="POST":
        email_id=request.POST.get("email_login")
        pwd=request.POST.get("password_login")
        el=list(user.objects.values('email'))
        #print(elist)
        print("OUTSIDE FIRST IF")
        elist=[]
        for i in el:
            elist.append(i['email'])
        print(elist)
        if email_id in elist:
            actual_pwd=list(user.objects.filter(email=email_id).values('password','user_id'))
            if actual_pwd[0]['password']==pwd:
                master_user_id=actual_pwd[0]['user_id']
                return render(request,'index.html')
            else:
                print("PASSWORD DID NOT MATCH")
                return render(request,'login.html')
        else:
            print("ALREADY USED EMAIL")
            return render(request,'login.html')
    return render(request,'login.html')

def register(request):
    global master_user_id
    if request.method=="POST":
        email_id=request.POST.get("mail")
        pwd1=request.POST.get("password1")
        pwd2=request.POST.get("password2")
        phn=request.POST.get("phone_num")
        uname=request.POST.get("username")
        elist=list(user.objects.values('email'))
        if email_id in elist:
            return render(request,'login.html')
        else:
            if pwd1 != pwd2:
                return render(request,'login.html')
            else:
                user_obj=user(user_name=uname,phn_num=phn,email=email_id,password=pwd1)
                user_obj.save()
                uid=list(user.objects.filter(email=email_id).values('user_id'))
                master_user_id=uid[0]
                return render(request,'index.html')
            #return render(request,'login.html')
    return render(request,'login.html')
def add_players(request):
    global sel_players_user
    global master_user_id
    global master_match_id
    if request.method=="POST":
        if master_user_id ==0:
            p=match_user.objects.filter(status='Did not start')
            msg="Sorry :( could not complete your request please logout and login and try again"
            return render(request,"createteam.html",{'error_msg':msg,"error":True,'matches':p})
        request.session['captain_choosen']=request.POST.getlist("captain")
        uteam=user_team(user_id=master_user_id,match_id=master_match_id,captain=request.session['captain_choosen'][0])
        uteam.save()
        uteam_id=user_team.objects.filter(user_id=master_user_id,match_id=master_match_id).values('id')
        for i in sel_players_user:
            cp=choosen_players(player_id=i,user_match_id=uteam_id,stars=0)
            cp.save()
    print(request.session['captain_choosen'][0],"is the captain choosen")
    p=match_user.objects.filter(status='Did not start')
    return render(request,"createteam.html",{'error_msg':"Succesfully created :)","error":True,'matches':p})
def update_scores_in_players(x):
    pass
def update_scores(request):
    global admin_match_id
    print(admin_match_id)
    if request.method=="POST":
        request.session['selected_batsmen']=request.POST.getlist("batsmen_ids_1")
        request.session['selected_bowler'] = request.POST.getlist("bowler_ids_1")
        request.session['selected_all_rounder'] = request.POST.getlist("ar_ids_1")
        request.session['selected_wicket_keeper']= request.POST.getlist("wk_ids_1")
        request.session['selected_batsmen_2']=request.POST.getlist("batsmen_ids_2")
        request.session['selected_bowler_2'] = request.POST.getlist("bowler_ids_2")
        request.session['selected_all_rounder_2'] = request.POST.getlist("ar_ids_2")
        request.session['selected_wicket_keeper_2']= request.POST.getlist("wk_ids_2")
        
        return render(request,'dummy.html')
    p=match_user.objects.filter(status='Did not start')
    q=country_team.objects.values('country').distinct()
    return render(request,'form.html',{"matches":p,"countries":q})


#player constrains
def constraints(request):
    global admin_match_id
    request.session['selected_batsmen']=request.POST.getlist("batsman_1")
    request.session['selected_bowler'] = request.POST.getlist("baller_1")
    request.session['selected_all_rounder'] = request.POST.getlist("allrounder_1")
    request.session['selected_wicket_keeper']= request.POST.getlist("wicketkeeper_1")
    request.session['selected_batsmen_2']=request.POST.getlist("batsman_2")
    request.session['selected_bowler_2'] = request.POST.getlist("baller_2")
    request.session['selected_all_rounder_2'] = request.POST.getlist("allrounder_2")
    request.session['selected_wicket_keeper_2']= request.POST.getlist("wicketkeeper_2")
    #print(request.session['selected_batsmen'])
    min_batsmen=4
    min_bowlers=3
    min_wk=1
    min_all=1
    all_players=11
    error_msg=[]
    all_selected_1=len(request.session['selected_batsmen'])+len(request.session['selected_bowler'])+len(request.session['selected_wicket_keeper'])+len(request.session['selected_all_rounder'])
    all_selected_2=len(request.session['selected_batsmen_2'])+len(request.session['selected_bowler_2'])+len(request.session['selected_wicket_keeper_2'])+len(request.session['selected_all_rounder_2'])
    if len(request.session['selected_batsmen'])<min_batsmen:
        error_msg.append("select minimum 4 batsmen for first country")
    if len(request.session['selected_bowler']) < min_bowlers:
        error_msg.append("select minimum 3 bowlers for first country")
    if len(request.session['selected_wicket_keeper']) < min_wk:
        error_msg.append("select minimum 1 wicket keeper for first country")
    if len(request.session['selected_all_rounder']) < min_all:
        error_msg.append("select minimum 1 all rounder for first country")
    if all_selected_1 != all_players:
        error_msg.append("select only 11 players for first country")
    if len(request.session['selected_batsmen_2'])<min_batsmen:
        error_msg.append("select minimum 4 batsmen for second country")
    if len(request.session['selected_bowler_2']) < min_bowlers:
        error_msg.append("select minimum 3 bowlers for second country")
    if len(request.session['selected_wicket_keeper_2']) < min_wk:
        error_msg.append("select minimum 1 wicket keeper for second country")
    if len(request.session['selected_all_rounder_2']) < min_all:
        error_msg.append("select minimum 1 all rounder for second country")
    if all_selected_2 != all_players:
        error_msg.append("select only 11 players for second country")
    if error_msg != []:
        return  render(request,'select_team.html',{'error_msg':error_msg,'error':True,'batsman_1':request.session['batsmen1'],'bowler_1':request.session['bowler1'],'allrounder_1':request.session['all_rounder1'],'wicketkeeper_1':request.session['wicket_keeper1'],'batsman_2':request.session['batsmen2'],'bowler_2':request.session['bowler2'],'allrounder_2':request.session['all_rounder2'],'wicketkeeper_2':request.session['wicket_keeper2']})
    print(request.session['selected_batsmen'])
    print(request.session['selected_bowler'])
    print(request.session['selected_all_rounder'])
    print(request.session['selected_wicket_keeper'])
    selected_batsmen_1 = []
    selected_bowler_1 = []
    selected_all_rounder_1 = []
    selected_wicket_keeper_1 = []
    for i in request.session['selected_batsmen']:
        selected_batsmen_1.append(country_team.objects.filter(player_id=int(i))[0])
    for i in request.session['selected_bowler']:
        selected_bowler_1.append(country_team.objects.filter(player_id=int(i))[0])
    for i in request.session['selected_wicket_keeper']:
        selected_wicket_keeper_1.append(country_team.objects.filter(player_id=int(i))[0])
    for i in request.session['selected_all_rounder']:
        selected_all_rounder_1.append(country_team.objects.filter(player_id=int(i))[0])
    selected_batsmen_2 = []
    selected_bowler_2 = []
    selected_all_rounder_2 = []
    selected_wicket_keeper_2 = []
    for i in request.session['selected_batsmen_2']:
        selected_batsmen_2.append(country_team.objects.filter(player_id=int(i))[0])
    for i in request.session['selected_bowler_2']:
        selected_bowler_2.append(country_team.objects.filter(player_id=int(i))[0])
    for i in request.session['selected_wicket_keeper_2']:
        selected_wicket_keeper_2.append(country_team.objects.filter(player_id=int(i))[0])
    for i in request.session['selected_all_rounder_2']:
        selected_all_rounder_2.append(country_team.objects.filter(player_id=int(i))[0])
    print(admin_match_id)
    return render(request,'update_scores.html',{'batsmanone_selected':selected_batsmen_1,'ballerone_selected':selected_bowler_1,'wicketkeeperone_selected':selected_wicket_keeper_1,'allrounderone_selected':selected_all_rounder_1,'batsmantwo_selected':selected_batsmen_2,'ballertwo_selected':selected_bowler_2,'wicketkeepertwo_selected':selected_wicket_keeper_2,'allroundertwo_selected':selected_all_rounder_2})


#creating a match
def create_match(request):
    coun1=request.POST.get('country1')
    coun2=request.POST.get('country2')
    error=[]
    if coun1 == coun2:
        error.append('Select two different countries')
        country_team_obj=country_team.objects.values('country').distinct()
        p=match_user.objects.filter(status='Did not start')
        return render(request,'form.html',{'error':error,'countries':country_team_obj,"matches":p})
    else:

        matchuserobj=match_user(country1=coun1,country2=coun2,status='Did not start')
        matchuserobj.save()
        error.append("SUCCESSFULLY CREATED A MATCH !!!")
        country_team_obj=country_team.objects.values('country').distinct()
        p=match_user.objects.filter(status='Did not start')
        return render(request,'form.html',{'error':error,'countries':country_team_obj,"matches":p})


#team selection
def select_team(request):
    global admin_match_id
    if request.method=="POST":
        request.session['match'] = request.POST["match"]
        match = request.session['match']
        admin_match_id=match
        # query = reduce(operator.or_,(Q(country=cn,category='bat') for cn in [country1,country2]))
        country1=match_user.objects.filter(match_id=match)[0].country1 
        country2 = match_user.objects.filter(match_id=match)[0].country2
        request.session['batsmen1'] = list(country_team.objects.filter(country=country1,category='Batsman').values())
        request.session['all_rounder1'] = list(country_team.objects.filter(country=country1,category='AllRounder').values())
        request.session['bowler1'] = list(country_team.objects.filter(country=country1,category='Bowler').values())
        request.session['wicket_keeper1']= list(country_team.objects.filter(country=country1,category__startswith='WicketKeeper').values())
        request.session['batsmen2'] = list(country_team.objects.filter(country=country2,category='Batsman').values())
        request.session['all_rounder2'] = list(country_team.objects.filter(country=country2,category='AllRounder').values())
        request.session['bowler2'] = list(country_team.objects.filter(country=country2,category='Bowler').values())
        request.session['wicket_keeper2']= list(country_team.objects.filter(country=country2,category__startswith='WicketKeeper').values())
        return  render(request,'select_team.html',{'batsman_1':request.session['batsmen1'],'bowler_1':request.session['bowler1'],'allrounder_1':request.session['all_rounder1'],'wicketkeeper_1':request.session['wicket_keeper1'],'batsman_2':request.session['batsmen2'],'bowler_2':request.session['bowler2'],'allrounder_2':request.session['all_rounder2'],'wicketkeeper_2':request.session['wicket_keeper2']})
    country_team_obj=country_team.objects.values('country').distinct()
    p=match_user.objects.filter(status='Did not start')
    error_msg="Sorry :( invalid selection "
    return render(request,'form.html',{'error':error,'countries':country_team_obj,"matches":p})


#index page
def index(request):
    global master_user_id
    print(master_user_id)
    return render(request,'index.html')


#player dashboard
def PlayerDashboard(request):
    global master_match_id
    master_match_id=0
    global master_user_id
    print(master_user_id)
    p=match_user.objects.filter(status='Completed')
    print(p)
	#return render(request,'playerdashboard.html',{"matches":p})
    #return render(request,'playerdashboard.html')
    return render(request,'playerdashboard.html',{"matches":p})

#team forming
def forming(request):
    p=match_user.objects.filter(status='Did not start')
    q=country_team.objects.values('country').distinct()
    return render(request,'form.html',{"matches":p,"countries":q})

#leaderboard
def Leaderboard(request):
    global master_match_id
    master_match_id=0
    global master_user_id
    print(master_user_id)
    p=match_user.objects.filter(status='Completed')
    return render(request,'leaderboard.html',{"matches":p})

    
def CreateTeam(request):
    global master_match_id
    master_match_id=0
    global master_user_id
    print(master_user_id)
    p=match_user.objects.filter(status='Did not start')
    return render(request,'createteam.html',{"matches":p})

#profile
def Profile(request):
    global master_match_id
    master_match_id=0
    global master_user_id
    if master_user_id==0:
        msg="Sorry :( could not complete your request please logout and login and try again"
        return render(request,"profile.html",{'error_msg':msg,"error":True})
    u_obj=list(user.objects.filter(user_id=master_user_id).values())
    l=list(user_team.objects.filter(user_id=master_user_id).values('match_id'))
    total=len(l)
    return render(request,'profile.html',{'user':u_obj,'k':total})


#create user team
def user_team_create(request):
    global points
    global sel_players_user
    global master_user_id
    print(master_user_id)
    if master_user_id ==0 :
        p=match_user.objects.filter(status='Did not start')
        msg="Sorry :( could not complete your request please logout and login and try again"
        return render(request,"createteam.html",{'error_msg':msg,"error":True,'matches':p})
    request.session['selected_batsmen']=request.POST.getlist("batsmen")
    request.session['selected_bowler'] = request.POST.getlist("bowler")
    request.session['selected_all_rounder'] = request.POST.getlist("all_rounder")
    request.session['selected_wicket_keeper']= request.POST.getlist("wicket_keeper")
    min_batsmen=4
    min_bowlers=3
    min_wk=1
    min_all=1
    all_players=11
    total_points=100
    selected_points=0
    error_msg=[]
    print(request.session['selected_batsmen'])
    request.session['selected_players'] = request.session['selected_batsmen'] + request.session['selected_bowler'] + request.session['selected_all_rounder'] + request.session['selected_wicket_keeper']
    for i in request.session['selected_batsmen']:
        selected_points+=country_team.objects.filter(player_id=int(i))[0].points
    for i in request.session['selected_bowler']:
        selected_points+=country_team.objects.filter(player_id=int(i))[0].points
    for i in request.session['selected_all_rounder']:
        selected_points+=country_team.objects.filter(player_id=int(i))[0].points
    for i in request.session['selected_wicket_keeper']:
        selected_points+=country_team.objects.filter(player_id=int(i))[0].points
    all_selected=len(request.session['selected_batsmen'])+len(request.session['selected_bowler'])+len(request.session['selected_wicket_keeper'])+len(request.session['selected_all_rounder'])
    print(len(request.session['selected_bowler'])," is the number of bowlers selected")
    if len(request.session['selected_batsmen'])<min_batsmen:
        error_msg.append("select minimum 4 batsmen")
    if len(request.session['selected_bowler']) < min_bowlers:
        error_msg.append("select minimum 3 bowlers")
    if len(request.session['selected_wicket_keeper']) < min_wk:
        error_msg.append("select minimum 1 wicket keeper")
    if len(request.session['selected_all_rounder']) < min_all:
        error_msg.append("select minimum 1 all rounder")
    if all_selected != all_players:
        error_msg.append("select only 11 players")
    if selected_points>total_points:
        error_msg.append("Select players with points less than 100")
    if error_msg != []:
        points = 100
        return  render(request,'ctm1.html',{'points':points,'error_msg':error_msg,'error':True,'batsmen':request.session['batsmen'],'bowler':request.session['bowler'],'all_rounder':request.session['all_rounder'],'wicket_keeper':request.session['wicket_keeper']})
    selected_batsmen = []
    selected_bowler = []
    selected_all_rounder = []
    selected_wicket_keeper = []
    for i in request.session['selected_batsmen']:
        selected_batsmen.append(country_team.objects.filter(player_id=int(i))[0])
        sel_players_user.append(int(i))
    for i in request.session['selected_bowler']:
        selected_bowler.append(country_team.objects.filter(player_id=int(i))[0])
        sel_players_user.append(int(i))
    for i in request.session['selected_wicket_keeper']:
        selected_wicket_keeper.append(country_team.objects.filter(player_id=int(i))[0])
        sel_players_user.append(int(i))
    for i in request.session['selected_all_rounder']:
        selected_all_rounder.append(country_team.objects.filter(player_id=int(i))[0])
        sel_players_user.append(int(i))
    # print("selected_batsmen",selected_batsmen)
    print(sel_players_user)
    return render(request,'ctm2.html',{'batsmen':selected_batsmen,'bowler':selected_bowler,'all_rounder':selected_all_rounder,'wicket_keeper':selected_wicket_keeper})

def Players_list(request):
    global points
    global master_match_id
    global master_user_id
    print(master_user_id)
    points=100
    if request.method=="POST":
        request.session['match'] = request.POST["match"]
        match = request.session['match']
        master_match_id=match
        matches_already=list(user_team.objects.filter(match_id=match,user_id=master_user_id))
        if matches_already != []:
            error_msg='You have already created a team for this match choose another match'
            p=match_user.objects.filter(status='Did not start')
            return render(request,'createteam.html',{'error_msg':error_msg,'error':True,'matches':p})
        if master_user_id==0:
            p=match_user.objects.filter(status='Did not start')
            msg="Sorry :( could not complete your request please logout and login and try again"
            return render(request,"createteam.html",{'error_msg':msg,"error":True,'matches':p})
        country1=match_user.objects.filter(match_id=match)[0].country1 
        country2 = match_user.objects.filter(match_id=match)[0].country2
        request.session['batsmen'] = list(country_team.objects.filter(country__in=[country1,country2],category='Batsman').values())
        request.session['all_rounder'] = list(country_team.objects.filter(country__in=[country1,country2],category='AllRounder').values())
        request.session['bowler'] = list(country_team.objects.filter(country__in=[country1,country2],category='Bowler').values())
        request.session['wicket_keeper']= list(country_team.objects.filter(country__in=[country1,country2],category__startswith='WicketKeeper').values())
        print(request.session['batsmen'])
        return  render(request,'ctm1.html',{'points':points,'batsmen':request.session['batsmen'],'bowler':request.session['bowler'],'all_rounder':request.session['all_rounder'],'wicket_keeper':request.session['wicket_keeper']})
    return render(request,'ctm1.html',{'points':points})
@csrf_exempt
def get_points(request):
    p_id = request.POST["id"]
    global points
    print("pid",p_id)
    print("points",points)
    p_points = country_team.objects.filter(player_id=p_id)
    if(int(request.POST["checked"])):
        new_points = int(points) - int(p_points[0].points)
        points = new_points
    else:
        new_points = int(points) + int(p_points[0].points)
        points = new_points

    return HttpResponse(new_points)
def leaderboardeval(request):
    global master_match_id
    master_match_id=0
    global master_user_id
    print(master_user_id)
    if request.method=="POST":
        request.session['match'] = request.POST["match"]
        match = request.session['match']
        uteams=list(user_team.objects.filter(match_id=match).values())
        ut=[]
        cp=[]
        us=[]
        lst=[]
        d={}
        for i in uteams:
            ut.append(i['id'])
            cp.append(i['captain'])
            us.append(i['user_id'])
        for j in ut:
            st=[]
            st=list(choosen_players.objects.filter(user_match=j).values('stars'))
            st1=[]
            score=0
            for k in st:
                st1.append(k['stars'])
            score=sum(st1)
            ind=ut.index(j)
            cap=cp[ind]
            s1=[]
            s1=list(choosen_players.objects.filter(player_id=cap,user_match_id=j).values())
            #print(s1,ind,cap,j)
            s2=s1[0]['stars']
            score+=s2
            lst.append(score)
            d[us[ind]]=score
        x={}
        x=sorted(d.items(),key =lambda kv:(kv[1],kv[0]),reverse=True)
        z=[]
        for h in x:
            print(h[0])
            y=[]
            y=list(user.objects.filter(user_id=h[0]).values())
            z.append(y)
        print(d)
        print(x)
        print(z)
        mylist=zip(x,z)
        mylist_2=zip(x,y)
        return render(request,'lbm1.html',{'d':mylist,'y':mylist_2})
    p=match_user.objects.filter(status='Completed')
    return render(request,'leaderboard.html',{"matches":p})
def pdm1(request):
    pass

# Create your views here.
