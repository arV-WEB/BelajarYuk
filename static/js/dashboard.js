/*=========================================================
    BELAJARYUK DASHBOARD
    dashboard.js
    Part 1
=========================================================*/

document.addEventListener("DOMContentLoaded", () => {

    initGreeting();
    initSearch();
    initNotification();
    initButtons();
    loadDashboardStats();

});


/*=========================================================
    GREETING
=========================================================*/

function initGreeting(){

    const title=document.querySelector(".header h1");

    if(!title) return;

    const hour=new Date().getHours();

    let greeting="";

    if(hour<12){

        greeting="Good Morning";

    }

    else if(hour<17){

        greeting="Good Afternoon";

    }

    else{

        greeting="Good Evening";

    }

    title.textContent=`${greeting}, Alex!`;

}


/*=========================================================
    SEARCH
=========================================================*/

function initSearch(){

    const input=document.querySelector(".search-box input");

    if(!input) return;

    input.addEventListener("focus",()=>{

        input.parentElement.classList.add("active");

    });

    input.addEventListener("blur",()=>{

        input.parentElement.classList.remove("active");

    });

}


/*=========================================================
    LIVE SEARCH DEMO
=========================================================*/

const searchInput=document.querySelector(".search-box input");

if(searchInput){

    searchInput.addEventListener("keyup",(e)=>{

        console.log("Searching:",e.target.value);

    });

}


/*=========================================================
    NOTIFICATION
=========================================================*/

function initNotification(){

    const bell=document.querySelector(".notification");

    if(!bell) return;

    bell.addEventListener("click",()=>{

        bell.classList.add("clicked");

        setTimeout(()=>{

            bell.classList.remove("clicked");

        },300);

        alert("You have 3 new notifications!");

    });

}


/*=========================================================
    BUTTON EFFECT
=========================================================*/

function initButtons(){

    const buttons=document.querySelectorAll("button");

    buttons.forEach(btn=>{

        btn.addEventListener("mousedown",()=>{

            btn.style.transform="scale(.96)";

        });

        btn.addEventListener("mouseup",()=>{

            btn.style.transform="";

        });

        btn.addEventListener("mouseleave",()=>{

            btn.style.transform="";

        });

    });

}


/*=========================================================
    MENU ACTIVE
=========================================================*/

const menu=document.querySelectorAll(".menu li");

menu.forEach(item=>{

    item.addEventListener("click",()=>{

        menu.forEach(m=>m.classList.remove("active"));

        item.classList.add("active");

    });

});


/*=========================================================
    PROFILE CLICK
=========================================================*/

const profile=document.querySelector(".profile");

if(profile){

    profile.addEventListener("click",()=>{

        alert("Profile page coming soon!");

    });

}


/*=========================================================
    ADD NOTE BUTTON
=========================================================*/

const addBtn=document.querySelector(".btn-primary");

if(addBtn){

    addBtn.addEventListener("click",()=>{

        alert("Create New Study Note");

    });

}


/*=========================================================
    VIEW ALL BUTTON
=========================================================*/

document.querySelectorAll(".btn-outline").forEach(btn=>{

    btn.addEventListener("click",()=>{

        alert("Showing all notes...");

    });

});


/*=========================================================
    TABLE HOVER
=========================================================*/

document.querySelectorAll("tbody tr").forEach(row=>{

    row.addEventListener("mouseenter",()=>{

        row.style.cursor="pointer";

    });

});


/*=========================================================
    CARD HOVER EFFECT
=========================================================*/

document.querySelectorAll(".card").forEach(card=>{

    card.addEventListener("mouseenter",()=>{

        card.style.transition=".3s";

    });

});


/*=========================================================
    WIDGET HOVER EFFECT
=========================================================*/

document.querySelectorAll(".widget").forEach(widget=>{

    widget.addEventListener("mouseenter",()=>{

        widget.style.transition=".3s";

    });

});


/*=========================================================
    LOG
=========================================================*/

console.log("BelajarYuk Dashboard Loaded Successfully");

/* ==========================================================
   DASHBOARD JS
   Part 2
   Search • Greeting • Stats Animation
========================================================== */


/* ==========================================================
   LIVE SEARCH
========================================================== */

const searchInput = document.querySelector(".search-box input");

const noteRows = document.querySelectorAll(".notes-table tbody tr");

if(searchInput){

    searchInput.addEventListener("keyup", function(){

        const keyword = this.value.toLowerCase();

        noteRows.forEach(row=>{

            const text = row.innerText.toLowerCase();

            if(text.includes(keyword)){

                row.style.display="table-row";

            }else{

                row.style.display="none";

            }

        });

    });

}


/* ==========================================================
   GREETING BY TIME
========================================================== */

const title = document.querySelector(".header h1");

if(title){

    const hour = new Date().getHours();

    let greeting="Welcome";

    if(hour>=5 && hour<12){

        greeting="Good Morning";

    }

    else if(hour>=12 && hour<17){

        greeting="Good Afternoon";

    }

    else if(hour>=17 && hour<21){

        greeting="Good Evening";

    }

    else{

        greeting="Good Night";

    }

    title.innerHTML=`${greeting}, Alex!`;

}


/* ==========================================================
   ACTIVE SIDEBAR
========================================================== */

const menuItems=document.querySelectorAll(".menu li");

menuItems.forEach(item=>{

    item.addEventListener("click",()=>{

        menuItems.forEach(i=>{

            i.classList.remove("active");

        });

        item.classList.add("active");

    });

});


/* ==========================================================
   NOTIFICATION BADGE
========================================================== */

const notification=document.querySelector(".notification");

if(notification){

    const badge=document.createElement("span");

    badge.className="notification-dot";

    badge.innerHTML="3";

    notification.appendChild(badge);

}


/* ==========================================================
   STATISTIC COUNT ANIMATION
========================================================== */

const stats=document.querySelectorAll(".card h2");

stats.forEach(stat=>{

    let value=stat.innerText;

    let target=parseInt(value);

    if(isNaN(target)) return;

    let count=0;

    let speed=Math.ceil(target/40);

    const timer=setInterval(()=>{

        count+=speed;

        if(count>=target){

            count=target;

            clearInterval(timer);

        }

        if(value.includes("h")){

            stat.innerHTML=count+"h";

        }else{

            stat.innerHTML=count;

        }

    },25);

});


/* ==========================================================
   BUTTON RIPPLE EFFECT
========================================================== */

const buttons=document.querySelectorAll("button");

buttons.forEach(button=>{

    button.addEventListener("click",function(e){

        const ripple=document.createElement("span");

        const rect=this.getBoundingClientRect();

        ripple.style.left=(e.clientX-rect.left)+"px";

        ripple.style.top=(e.clientY-rect.top)+"px";

        ripple.className="ripple";

        this.appendChild(ripple);

        setTimeout(()=>{

            ripple.remove();

        },600);

    });

});

/* ==========================================================
   DASHBOARD JS
   Part 3
   Animation • LocalStorage • Shortcuts
========================================================== */


/* ==========================================================
   PROGRESS BAR ANIMATION
========================================================== */

const progressFill=document.querySelector(".progress-fill");

if(progressFill){

    progressFill.style.width="0%";

    setTimeout(()=>{

        progressFill.style.transition="width 1.5s ease";

        progressFill.style.width="75%";

    },300);

}


/* ==========================================================
   SAVE SEARCH TO LOCAL STORAGE
========================================================== */

if(searchInput){

    const lastSearch=localStorage.getItem("dashboardSearch");

    if(lastSearch){

        searchInput.value=lastSearch;

        searchInput.dispatchEvent(new Event("keyup"));

    }

    searchInput.addEventListener("keyup",()=>{

        localStorage.setItem(
            "dashboardSearch",
            searchInput.value
        );

    });

}


/* ==========================================================
   CTRL + K SHORTCUT
========================================================== */

document.addEventListener("keydown",(e)=>{

    if(e.ctrlKey && e.key.toLowerCase()=="k"){

        e.preventDefault();

        searchInput.focus();

        searchInput.select();

    }

});


/* ==========================================================
   CARD GLOW EFFECT
========================================================== */

const cards=document.querySelectorAll(".card");

cards.forEach(card=>{

    card.addEventListener("mousemove",(e)=>{

        const rect=card.getBoundingClientRect();

        const x=e.clientX-rect.left;

        const y=e.clientY-rect.top;

        card.style.background=

        `radial-gradient(circle at ${x}px ${y}px,
        rgba(79,125,243,.15),
        white 65%)`;

    });

    card.addEventListener("mouseleave",()=>{

        card.style.background="white";

    });

});


/* ==========================================================
   SMOOTH SCROLL
========================================================== */

document.querySelectorAll("a[href^='#']").forEach(anchor=>{

    anchor.addEventListener("click",function(e){

        e.preventDefault();

        const target=document.querySelector(
            this.getAttribute("href")
        );

        if(target){

            target.scrollIntoView({

                behavior:"smooth"

            });

        }

    });

});


/* ==========================================================
   WIDGET FADE-IN
========================================================== */

const observer=new IntersectionObserver((entries)=>{

    entries.forEach(entry=>{

        if(entry.isIntersecting){

            entry.target.classList.add("show-widget");

        }

    });

},{
    threshold:.2
});

document.querySelectorAll(".widget").forEach(widget=>{

    observer.observe(widget);

});


/* ==========================================================
   ACHIEVEMENT HOVER
========================================================== */

document.querySelectorAll(".achievement-card")
.forEach(card=>{

    card.addEventListener("mouseenter",()=>{

        card.style.transform="translateY(-4px)";

    });

    card.addEventListener("mouseleave",()=>{

        card.style.transform="translateY(0)";

    });

});


/* ==========================================================
   DEADLINE HOVER
========================================================== */

document.querySelectorAll(".deadline-item")
.forEach(item=>{

    item.addEventListener("mouseenter",()=>{

        item.style.background="#F8FAFC";

    });

    item.addEventListener("mouseleave",()=>{

        item.style.background="transparent";

    });

});


/* ==========================================================
   PAGE LOADED
========================================================== */

window.addEventListener("load",()=>{

    document.body.classList.add("loaded");

});

/* ==========================================================
   DASHBOARD JS
   Part 4 (Final)
========================================================== */


/* ==========================================================
   DARK MODE
========================================================== */

const darkButton=document.createElement("button");

darkButton.className="dark-mode-btn";

darkButton.innerHTML='<i class="bi bi-moon-stars"></i>';

document.querySelector(".top-right").prepend(darkButton);

if(localStorage.getItem("theme")=="dark"){

    document.body.classList.add("dark");

}

darkButton.onclick=()=>{

    document.body.classList.toggle("dark");

    if(document.body.classList.contains("dark")){

        localStorage.setItem("theme","dark");

    }else{

        localStorage.setItem("theme","light");

    }

}


/* ==========================================================
   REALTIME CLOCK
========================================================== */

const clock=document.createElement("div");

clock.className="clock";

document.querySelector(".topbar").appendChild(clock);

function updateClock(){

    const now=new Date();

    clock.innerHTML=

    now.toLocaleDateString()+" | "+now.toLocaleTimeString();

}

setInterval(updateClock,1000);

updateClock();


/* ==========================================================
   TOAST NOTIFICATION
========================================================== */

function showToast(message){

    const toast=document.createElement("div");

    toast.className="toast";

    toast.innerHTML=message;

    document.body.appendChild(toast);

    setTimeout(()=>{

        toast.classList.add("show");

    },100);

    setTimeout(()=>{

        toast.classList.remove("show");

        setTimeout(()=>{

            toast.remove();

        },300);

    },3000);

}


/* ==========================================================
   WELCOME
========================================================== */

window.addEventListener("load",()=>{

    showToast("👋 Welcome back, Alex!");

});


/* ==========================================================
   AUTO REFRESH DEMO
========================================================== */

setInterval(()=>{

    const badge=document.querySelector(".notification-dot");

    if(badge){

        let value=parseInt(badge.innerHTML);

        value++;

        badge.innerHTML=value;

    }

},30000);


/* ==========================================================
   ADD NOTE BUTTON
========================================================== */

const addButton=document.querySelector(".btn-primary");

if(addButton){

    addButton.addEventListener("click",()=>{

        showToast("Feature will be connected to database.");

    });

}


/* ==========================================================
   VIEW ALL BUTTON
========================================================== */

document.querySelectorAll(".btn-outline").forEach(btn=>{

    btn.onclick=()=>{

        showToast("Opening Study Notes...");

    }

});


/* ==========================================================
   SETTINGS
========================================================== */

const setting=document.querySelector(".sidebar-bottom");

if(setting){

    setting.onclick=()=>{

        showToast("Settings page coming soon.");

    }

}


/* ==========================================================
   MENU CLICK
========================================================== */

document.querySelectorAll(".menu li").forEach(item=>{

    item.onclick=()=>{

        showToast(item.innerText.trim());

    }

});

// ==============================
// Dashboard Statistics
// ==============================

const dashboardStats = {
    totalNotes: 128,
    studyHours: 142,
    activeGoals: 12,
    deadlines: 3
};


function loadDashboardStats() {

    document.getElementById("totalNotes").textContent =
        dashboardStats.totalNotes;

    document.getElementById("studyHours").textContent =
        dashboardStats.studyHours + "h";

    document.getElementById("activeGoals").textContent =
        dashboardStats.activeGoals;

    document.getElementById("deadlines").textContent =
        dashboardStats.deadlines;

}
/* ==========================================================
   END
========================================================== */

console.log("BelajarYuk Dashboard Ready.");