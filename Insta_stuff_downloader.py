#Importing Modules
from tkinter import *
from PIL import ImageTk,Image
import instaloader
from tkcalendar import DateEntry
import datetime
import tkinter.messagebox as mg
import os
import requests
import re
import random
import string
import sqlite3
from tkinter import ttk

#Joining instaloader
L=instaloader.Instaloader()

#creating Database
connector = sqlite3.connect('Instarecords.db')
cursor = connector.cursor()
connector.execute("CREATE TABLE IF NOT EXISTS Insta_records (STUDENT_ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,DATE TEXT, USERNAME TEXT, TARGETUSER TEXT, POST TEXT, STORIES TEXT, HIGHLIGHTS TEXT,TAGGED TEXT,IGTV TEXT)")

#Saving Data into database
def save_data():
    name=user_name.get()
    tar= target_user.get()
    ID_POST= id_posts.get()
    STORIES = stories.get()
    HIGHLIGTS = highlights.get()
    TAGGED = tagges.get()
    IGTV=igtv.get()
    date=datetime.datetime.now()
    connector.execute('INSERT INTO Insta_records (DATE,USERNAME,TARGETUSER, POST, STORIES, HIGHLIGHTS,TAGGED,IGTV) VALUES (?,?,?,?,?,?,?,?)', (date,name, tar, str(ID_POST), str(STORIES),str(HIGHLIGTS),str(TAGGED),str(IGTV)))
    connector.commit()


#Admin View
def admin():
    global id_posts,stories,highlights,profile_pic,tagges,igtv,since,until,target_user,user_name,pass_word,link,tree,connector
    app=Tk()
    app.geometry("1080x500")

    #Display records
    def display_records():
        global id_posts,stories,highlights,profile_pic,tagges,igtv,since,until,target_user,user_name,pass_word,link,tree,connector
        #tree.delete(*tree.get_children())

        curr = connector.execute('SELECT * FROM Insta_records')
        data = curr.fetchall()

        for records in data:
            tree.insert('', END, values=records)


    #delete record
    def remove_record():
        if not tree.selection():
            mg.showerror('Error!', 'Please select an item from the database')
        else:
            current_item = tree.focus()
            values = tree.item(current_item)
            selection = values["values"]

            tree.delete(current_item)

            connector.execute('DELETE From Insta_records where STUDENT_ID=%d' % selection[0])
            connector.commit()

            mg.showinfo('Done', 'The record you wanted deleted was successfully deleted.')

            display_records()


    
    tree = ttk.Treeview(app, height=100, selectmode=BROWSE,
                    columns=('ID',"DATE", "USERNAME", "TARGETUSER","POST", "STORIES", "HIGHLIGHTS", "TAGGED", "IGTV"))

    X_scroller = Scrollbar(tree, orient=HORIZONTAL, command=tree.xview)
    Y_scroller = Scrollbar(tree, orient=VERTICAL, command=tree.yview)

    X_scroller.pack(side=BOTTOM, fill=X)
    Y_scroller.pack(side=RIGHT, fill=Y)

    tree.config(yscrollcommand=Y_scroller.set, xscrollcommand=X_scroller.set)

    tree.heading('ID', text='ID', anchor=CENTER)
    tree.heading('DATE', text='DATE', anchor=CENTER)
    tree.heading('USERNAME', text='USERNAME', anchor=CENTER)
    tree.heading('TARGETUSER', text='TARGETUSER', anchor=CENTER)
    tree.heading('POST', text='POST', anchor=CENTER)
    tree.heading('STORIES', text='STORIES', anchor=CENTER)
    tree.heading('HIGHLIGHTS', text='HIGHLIGHTS', anchor=CENTER)
    tree.heading('TAGGED', text='TAGGED', anchor=CENTER)
    tree.heading('IGTV', text='IGTV', anchor=CENTER)

    tree.column('#0', minwidth=0, stretch=NO)
    tree.column('#1', minwidth=100, stretch=NO)
    tree.column('#2', minwidth=80, stretch=NO)
    tree.column('#3', minwidth=80, stretch=NO)
    tree.column('#4', minwidth=10, stretch=NO)
    tree.column('#5', minwidth=10, stretch=NO)
    tree.column('#6', minwidth=10, stretch=NO)
    tree.column('#7', minwidth=10, stretch=NO)
    tree.column('#8', minwidth=10, stretch=NO)
    tree.column('#9', minwidth=150, stretch=NO)

    tree.place(y=0, relwidth=1, relheight=0.6, relx=0)
    Button(app,text="delete record",command=remove_record).pack(side=BOTTOM)
    display_records()
    app.update()
    app.mainloop()
    pass

#Downlad post
def post_download(SINCE,UNTIL,user):
    profile = instaloader.Profile.from_username(L.context,user)
    for post in profile.get_posts():
        if SINCE<post.date<UNTIL:
            L.download_post(post, target=profile.username)
        elif post.date<SINCE:
            break

#Download stories
def story_download(user):
    L.download_profile(user,download_stories_only=True)

#Download Hightlights
def highlight_download(SINCE,UNTIL,user):

    profile = instaloader.Profile.from_username(L.context,user)
    for post in profile.get_posts():
        if SINCE<post.date<UNTIL:
            L.download_highlights(profile)
        elif post.date<SINCE:
            break

#Download profile pic
def profile_pic_download(user):  
    L.download_profile(user,profile_pic_only=True)

#Download IGTV videos'
def igtv_download(SINCE,UNTIL,user):
    profile = instaloader.Profile.from_username(L.context,user)
    for post in profile.get_igtv_posts():
        if SINCE<post.date<UNTIL:
            L.download_igtv(post)
        elif post.date<SINCE:
            break

#download Tegged posts
def tagges_download(SINCE,UNTIL,user):
    profile = instaloader.Profile.from_username(L.context,user)
    for post in profile.get_tagged_posts():
        if SINCE<post.date<UNTIL:
            L.download_tagged(profile)
        elif post.date<SINCE:
            break

#opening file location
def open_folder():
    try:
        hashta=has.get()
        hashta='#'+hashta
        folder=os.path.dirname(__file__)+"\\"+hashta
        os.startfile(folder)
    except:
        user=target_user.get()
        if user.startswith("https"):
        #https://instagram.com/handemiyy?igshid=YmMyMTA2M2Y=
            user=user.split("/")
            user,a=user[-1].split("?")
        folder=os.path.dirname(__file__)+"\\"+user
        os.startfile(folder)
        
#Creating a Tkinter GUI Window
root=Tk()
root.geometry("640x700")
root.resizable(0, 0)
root.title("Instagram Downloader")

#Backgroung Image
#img=Image.open(r"C:\Users\prath\OneDrive\Desktop\codes\photo_2022-04-24_17-11-43.jpg")
#img=img.resize((640,800), resample=Image.LANCZOS)
#bg_image=ImageTk.PhotoImage(img)
#Label(root , image=bg_image).pack()

#Downloading from instagram
def download_from_insta():
    global id_posts,stories,highlights,profile_pic,tagges,igtv,since,until,target_user
    k=since.get()
    
    k=k.split("/")
    k[2]="20"+k[2]
    since_new=datetime.datetime(int(k[2]),int(k[0]),int(k[1]))
    
    m=until.get()
    m=m.split("/")
    m[2]="20"+m[2]
    until_new=datetime.datetime(int(m[2]),int(m[0]),int(m[1])) 
    
    user=target_user.get()
    
    if user.startswith("https"):
    #https://instagram.com/handemiyy?igshid=YmMyMTA2M2Y=
        user=user.split("/")
        user,a=user[-1].split("?")
        pass
     
    try:
        L.check_profile_id(user)
        save_data()

        if id_posts.get():
            post_download(since_new,until_new,user)
            
        if stories.get():
            story_download(user)
            
        if highlights.get():
            highlight_download(since_new,until_new,user)
            
        if profile_pic.get():
            profile_pic_download(user)
            
        if tagges.get():
            tagges_download(since_new,until_new,user)

        if igtv.get():
            igtv_download(since_new,until_new,user)

        mg.showinfo("Done!","Every thing has been downloaded")
        
        Button(root,text="Open folder",bg="white",fg="red",activebackground="red",activeforeground="white",command=open_folder).place(x=250,y=630)
    
    except:
        mg.showerror("Error","Invalid username or not in following")

#Entering data into the Application
def input_for_download():
    global id_posts,stories,highlights,profile_pic,tagges,igtv,until,since,target_user
    global dfu1,dfu2,dfu3,dfp1,dfp2,dfp3,dfp4,dfp5,dfp6,ifd1,ifd2,ifd3,ifd4,ifd5,c1,c2,c3,c4,c5,c6
    try:
        dfp6.destroy()
    except:
        pass
    target_user=StringVar()
    ifd1=Label(root,text="Enter the username of target account",font=('Arial',13),bg='pink')
    ifd1.place(x=200,y=340)
    ifd2=Entry(root,textvariable=target_user)
    ifd2.place(x=200,y=375)
    
    id_posts=BooleanVar()
    c1=Checkbutton(root,text="Posts",variable=id_posts,offvalue=False,onvalue=True,font=('arial',13),bg='pink')
    c1.place(x=200,y=400)
    
    stories=BooleanVar()
    c2=Checkbutton(root,text="Stories",variable=stories,offvalue=False,onvalue=True,font=('arial',13),bg='pink')
    c2.place(x=200,y=435)
    
    highlights=BooleanVar()
    c3=Checkbutton(root,text="Highlights",variable=highlights,offvalue=False,onvalue=True,font=('arial',13),bg='pink')
    c3.place(x=200,y=470)
    
    profile_pic=BooleanVar()
    c4=Checkbutton(root,text="Profile pic",variable=profile_pic,offvalue=False,onvalue=True,font=('arial',13),bg='pink')
    c4.place(x=200,y=505)
    
    tagges=BooleanVar()
    c5=Checkbutton(root,text="Tagged",variable=tagges,offvalue=False,onvalue=True,font=('arial',13),bg='pink')
    c5.place(x=200,y=540)
    
    igtv=BooleanVar()
    c6=Checkbutton(root,text="Tagges",variable=igtv,offvalue=False,onvalue=True,font=('arial',13),bg='pink')
    c6.place(x=200,y=540)
    
    ifd3=Button(root,text="Start downloading",bg="white",fg="red",activebackground="red",activeforeground="white",command=download_from_insta)
    ifd3.place(x=250,y=580)
    
    ifd4=Label(root,text="Since",font=('Arial',13),bg='pink')
    ifd4.place(x=300,y=400)
    since = DateEntry(root, font=("Arial", 12), width=15)
    since.place(x=300,y=425)
    
    ifd5=Label(root,text="Until",font=('Arial',13),bg='pink')
    ifd5.place(x=480,y=400)
    until = DateEntry(root, font=("Arial", 12), width=15)
    until.place(x=480,y=425)

#Checking Login Details
def check_username():

    global id_posts,stories,highlights,profile_pic,tagges,igtv,since,until,target_user,user_name,pass_word
    global radio_for_hasa
    user=user_name.get()
    password=pass_word.get()
    if user=="admin":
        if password=="hello":
            admin()
        else:
            mg.showerror("Error","Wrong password")
    else:  
        try:
            L.login(user,password)
            if radio_for_hasa.get()==0:
                input_for_download()
            else:
                download_from_hashtag()

        except:
       
            mg.showerror("Error","Invalid username or password")
    
#If downloading from profile
def download_from_profile():
    global id_posts,stories,highlights,profile_pic,tagges,igtv,since,until,target_user,user_name,pass_word
    global dfu1,dfu2,dfu3,dfp1,dfp2,dfp3,dfp4,dfp5,dfp6,ifd1,ifd2,ifd3,ifd4,ifd5,c1,c2,c3,c4,c5,c6,dfhl1,dfhl2,dfhe1,dfhe2,dfhb
    global radio_for_hasa
    user_name=StringVar()
    pass_word=StringVar()

    dfp1=Label(root,text="Login",font=('Arial',15),bg='pink')
    dfp1.place(x=200,y=150)
    
    dfp2=Label(root,text="Username",font=('Arial',13),bg='pink')
    dfp2.place(x=200,y=200)
    dfp3=Entry(root,textvariable=user_name)
    dfp3.place(x=300,y=200)
    
    dfp4=Label(root,text="Password",font=('Arial',13),bg='pink')
    dfp4.place(x=200,y=250)
    dfp5=Entry(root,textvariable=pass_word,show='*')
    dfp5.place(x=300,y=250)
    
    dfp6=Frame(root,bg="pink")
    dfp6.place(x=200,y=300)
    radio_for_hasa=IntVar()
    r=Radiobutton(dfp6,text="Download from profile",variable=radio_for_hasa,value=0,bg='pink').pack()
    r=Radiobutton(dfp6,text="Download from Hashtag",variable=radio_for_hasa,value=1,bg='pink').pack()
    Button(dfp6,text="Login in",bg="white",fg="red",activebackground="red",activeforeground="white",command=check_username).pack()
    
    try:
        dfu1.destroy()
        dfu2.destroy()
        dfu3.destroy()
    except:
        pass
    try:
        ifd1.destroy()
        ifd2.destroy()
        ifd3.destroy()
        ifd4.destroy()
        ifd5.destroy()
        c1.destroy()
        c2.destroy()
        c3.destroy()
        c4.destroy()
        c5.destroy()
        c6.destroy()
        since.destroy()
        until.destroy()
    except:
        pass
    try:
        dfhl1.destroy()
        dfhl2.destroy()
        dfhe1.destroy()
        dfhe2.destroy()
        dfhb.destroy()
    except:
        pass
    
#if downloading from url
def url_download():
    global id_posts,stories,highlights,profile_pic,tagges,igtv,since,until,target_user,user_name,pass_word,link
    def get_response(url):
        r = requests.post(url)
        while r.status_code != 200:
            r = requests.get(url)
        return r.text

    def prepare_urls(matches):
        return list({match.replace("\\u0026", "&") for match in matches})


    url = link.get()
    response = get_response(url)

    vid_matches = re.findall('"video_url":"([^"]+)"', response)
    pic_matches = re.findall('"display_url":"([^"]+)"', response)

    vid_urls = prepare_urls(vid_matches)
    pic_urls = prepare_urls(pic_matches)
    if vid_urls or pic_urls:
        if vid_urls:
            chunk_sixe=256
            for ur in vid_urls:
                letters=string.ascii_letters
                result_str=''.join(random.choice(letters)for i in range(6))
                
                r=requests.get(ur,stream=True)
                with open(f"{result_str}.mp4","wb")as f:
                    for chuck in r.iter_content(chunk_size=chunk_sixe):
                        f.write(chuck)
            
        
    #https://www.instagram.com/reel/CdfAH8Vl5EL/?utm_source=ig_web_copy_link
    #https://www.instagram.com/p/CdDv3qssIEY/?utm_source=ig_web_copy_link
        if pic_urls:
            chunk_sixe=256
            for ur in pic_urls:
                letters=string.ascii_letters
                result_str=''.join(random.choice(letters)for i in range(6))
                r=requests.get(ur,stream=True)
                with open(f"{result_str}.jpg","wb")as f:
                    for chuck in r.iter_content(chunk_size=chunk_sixe):
                        f.write(chuck)
        mg.showinfo("",'Downloaded')
    else:
        mg.showerror("","The content can't be downloaded due to login issue try to download from profile")
        download_from_profile()


def download_from_url():
    global id_posts,stories,highlights,profile_pic,tagges,igtv,since,until,target_user,user_name,pass_word,link
    global dfu1,dfu2,dfu3,dfp1,dfp2,dfp3,dfp4,dfp5,dfp6,ifd1,ifd2,ifd3,ifd4,ifd5,c1,c2,c3,c4,c5,c6,dfhl1,dfhl2,dfhe1,dfhe2,dfhb


    dfu1=Label(root,text="Enter url",font=('Arial',13),bg='pink')
    dfu1.place(x=150,y=140)
    link=StringVar()
    dfu2=Entry(root,textvariable=link)
    dfu2.place(x=250,y=140)

    dfu3=Button(root,text="Download",command=url_download,bg="white",fg="red",activebackground="red",activeforeground="white",font=('Arial',11))
    dfu3.place(x=200,y=170)
    
    try:
        dfp1.destroy()
        dfp2.destroy()
        dfp3.destroy()
        dfp4.destroy()
        dfp5.destroy()
        dfp6.destroy()
    except:
        pass
    try:
        ifd1.destroy()
        ifd2.destroy()
        ifd3.destroy()
        ifd4.destroy()
        ifd5.destroy()
        c1.destroy()
        c2.destroy()
        c3.destroy()
        c4.destroy()
        c5.destroy()
        c6.destroy()
        since.destroy()
        until.destroy()
    except:
        pass
    try:
        dfhl1.destroy()
        dfhl2.destroy()
        dfhe1.destroy()
        dfhe2.destroy()
        dfhb.destroy()
    except:

        pass
def load_hashtag():
    global has,max_co
    hashta=has.get()
    max_coun=int(max_co.get())
    try:
        L.download_hashtag(hashta,max_count=max_coun)
        mg.showinfo("Downloaded",f"Post from {hashta} has been downloaded")
        Button(root,text="Open folder",bg="white",fg="red",activebackground="red",activeforeground="white",command=open_folder).place(x=250,y=630)

    except:
        mg.showerror("","Hashtag id either blocked or not visible in your country or try to login first and then enter the Hashtag")


    pass
def download_from_hashtag():
    global has,max_co
    global dfhl1,dfhl2,dfhe1,dfhe2,dfhb
    has=StringVar()
    max_co=StringVar()
    dfhl1=Label(root,text="Hashtag",font=('Arial',13),bg='pink')
    dfhl1.place(x=150,y=140)
    dfhe1=Entry(root,textvariable=has)
    dfhe1.place(x=250,y=140)
    dfhl2=Label(root,text="Max count",font=('Arial',13),bg='pink')
    dfhl2.place(x=150,y=170)
    dfhe2=Entry(root,textvariable=max_co)
    dfhe2.place(x=250,y=170)
    dfhb=Button(root,text="Download",bg="white",fg="red",activebackground="red",activeforeground="white",command=load_hashtag,font=('Arial',11))
    dfhb.place(x=200,y=230)
    try:
        dfp1.destroy()
        dfp2.destroy()
        dfp3.destroy()
        dfp4.destroy()
        dfp5.destroy()
        dfp6.destroy()
    except:
        pass
    try:
        dfu1.destroy()
        dfu2.destroy()
        dfu3.destroy()
    except:
        pass
    try:
        ifd1.destroy()
        ifd2.destroy()
        ifd3.destroy()
        ifd4.destroy()
        ifd5.destroy()
        c1.destroy()
        c2.destroy()
        c3.destroy()
        c4.destroy()
        c5.destroy()
        c6.destroy()
        since.destroy()
        until.destroy()
    except:

        pass
#main buttons
Button(root,text="Download from url(Reels)",bg="white",fg="red",activebackground="red",activeforeground="white",command=download_from_url ,font=('Arial',11)).place(x=100,y=100)
Button(root,text="Login to download",command=download_from_profile,bg="white",fg="red",activebackground="red",activeforeground="white",font=('Arial',11)).place(x=290,y=100)
Button(root,text="Download Hashtag",command=download_from_hashtag,bg="white",fg="red",activebackground="red",activeforeground="white",font=('Arial',11)).place(x=425,y=100)
Button(root,text="History",command=admin,bg="white",fg="red",activebackground="red",activeforeground="white",font=('Arial',11)).place(x=550,y=10)

root.update()
root.mainloop()