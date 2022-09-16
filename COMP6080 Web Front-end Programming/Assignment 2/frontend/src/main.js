import { BACKEND_PORT } from './config.js';
// A helper you may want to use when uploading new images to the server.
import { fileToDataUrl} from './helpers.js';


let authToken = null;
let authUserID = null;
let storeUserID = null;
let authEmail = null;
let storeEmail = null;
let authName = null;
let storePassword = null;
let storeImage=null;
let authImage="";
let jobImage="";
let newJobImage="";
let jobStoreImage="";
let storeJobId=null;
let storeJobImage=null;
let storeJobTitle=null;
let storeJobDescription=null;
let storeJobStart=null;

const formatTime = (timestamp) => {
    let result;
    var time = new Date(timestamp);
    var curr = new Date();
    var diff_in_time = curr.getTime() - time.getTime();
    var diff_in_day = diff_in_time / (1000 * 3600 * 24);
    var diff_in_hour = diff_in_time / (1000 * 3600);
    var diff_in_minutes = diff_in_time / (1000 * 60);
    if (diff_in_day >= 1) {
        result = time.getDate() + '/' + (time.getMonth() + 1) + '/' + time.getFullYear();
    } else if (diff_in_hour >= 1) {
        result = Math.floor(diff_in_hour) + ' hours ago';
    } else {
        result = Math.floor(diff_in_minutes) + ' minutes ago';
    }
    return result;
};

const apiCall =(path, method, body) => {
    return new Promise((resolve, reject) => {
        const init = {
            method: method,
            headers: {
                'Content-Type': 'application/json',
                Authorization: (path === 'auth/register' || path === 'auth/login') ? undefined : authToken,
            },
            body: method === 'GET' ? undefined : JSON.stringify(body),
        };
    
        fetch(`http://localhost:${BACKEND_PORT}/${path}`, init)
            .then(response=>response.json())
            .then(body => { 
                if (body.error) {
                    // alert(body.error);
                    document.getElementById("error-message").textContent = body.error;
		            document.getElementById("error-popup").style.display = "block";
                } else {
                    resolve(body);
                }
            });
    })
    
};

const register = (email, password, name) => {
    return apiCall('auth/register', 'POST', {
        email,
        password,
        name,
    });
    
};

const login = (email, password) => {
    return apiCall('auth/login', 'POST', {
        email,
        password,
    });
};

const getProfile = (userID) => {
    return apiCall(`user?userId=${userID}`, 'GET', {});
};

const getJobList = (startIndex) => {
    apiCall(`job/feed?start=${startIndex}`, 'GET', {}).then((body)=> {
        for (let i = startIndex; i < body.length; i++) {
            let data=body[i];
            //console.log(data);
            let index = i;
            let jobID= data.id;
            //console.log(jobID);
            let titleFeed = data.title;
            let imageLink = data.image;
            let startDate = new Date(data.start);
            startDate = startDate.getDate() + '/' + (startDate.getMonth() + 1) + '/' + startDate.getFullYear();
            let descriptionFeed = data.description;
            let postTime = formatTime(data.createdAt);
            let likeFeed = data.likes;
            let commentsFeed = data.comments;
            getProfile(data.creatorId).then(items => {
                let authName = items.name;
                
                // create job card
                let jobCard = document.createElement('div');
                jobCard.setAttribute('id', 'jobCard');
                document.getElementById('feed-screen').appendChild(jobCard);
                
                //left part
                let leftPart = document.createElement('div');
                leftPart.setAttribute('class', 'leftPart');
                jobCard.appendChild(leftPart);
                
                //right part
                let rightPart = document.createElement('div');
                rightPart.setAttribute('class', 'rightPart');
                jobCard.appendChild(rightPart);

                // image part
                let imagePart=document.createElement('div');
                let picInfo=document.createElement('img');
                picInfo.setAttribute('id', 'picInfo');
                picInfo.src = imageLink;
                imagePart.appendChild(picInfo);
                leftPart.appendChild(imagePart);

                // name part
                let namePart = document.createElement('span');
                namePart.setAttribute('id', 'author');
                namePart.innerText=authName;
                namePart.addEventListener('click', () => {
                    authUserID=data.creatorId;
                    gotoProfileScreen();
                });
                leftPart.appendChild(namePart);
                
                // like and dislike button
                let likeControlPart = document.createElement('div');
                likeControlPart.setAttribute('class', 'likeControlPart');
                leftPart.appendChild(likeControlPart);
                
                // like button
                let likeButton=document.createElement('input');
                likeButton.setAttribute('type', 'button');
                likeButton.setAttribute('class', 'Like');
                likeButton.setAttribute('value', 'Like');
                likeButton.addEventListener('click', () => {
                    apiCall('job/like', 'PUT', {
                        id: jobID,
                        turnon: true,
                    });
                    gotoWelcomeScreen();
                });
                likeControlPart.appendChild(likeButton);

                // dislike button
                let dislikeButton=document.createElement('input');
                dislikeButton.setAttribute('type', 'button');
                dislikeButton.setAttribute('class', 'Dislike');
                dislikeButton.setAttribute('value', 'Dislike');
                dislikeButton.addEventListener('click', () => {
                    apiCall('job/like', 'PUT', {
                        id: jobID,
                        turnon: false,
                    });
                    gotoWelcomeScreen();
                });
                likeControlPart.appendChild(dislikeButton);

                // title
                let titlePart=document.createElement('h2');
                titlePart.setAttribute('class', 'jobTitle');
                titlePart.innerText=titleFeed;
                rightPart.appendChild(titlePart);

                // post time
                let postTimePart=document.createElement('h5');
                postTimePart.setAttribute('class', 'postTime');
                postTimePart.innerText='Post at: '+postTime;
                rightPart.appendChild(postTimePart);

                // combine description & start Time
                let divPart = document.createElement('div');
                rightPart.appendChild(divPart);

                // description 
                let descriptionPart=document.createElement('h3');
                descriptionPart.setAttribute('class', 'jobDescription');
                descriptionPart.innerText=descriptionFeed;
                divPart.appendChild(descriptionPart);

                // start Time
                let startTimePart=document.createElement('h5');
                startTimePart.setAttribute('class', 'startTime');
                startTimePart.innerText='Start at: '+startDate;
                divPart.appendChild(startTimePart);

                // like and comments amount
                let amountPart = document.createElement('div');
                amountPart.setAttribute('class', 'showAmount');
                rightPart.appendChild(amountPart);
                let likeText = document.createElement('div');
                likeText.setAttribute('class','likeText');
                likeText.innerText='Likes: '+likeFeed.length;
                let commentsText = document.createElement('div');
                commentsText.setAttribute('class','commnetsText');
                commentsText.innerText='Comments: '+commentsFeed.length;
                amountPart.appendChild(likeText);
                amountPart.appendChild(commentsText);

                // comments input and send
                let commentsSendPart = document.createElement('div');
                commentsSendPart.setAttribute('class', 'commentsSend');
                rightPart.appendChild(commentsSendPart);
                let commentsInput=document.createElement('input');
                commentsInput.setAttribute('type', 'text');
                commentsInput.setAttribute('class', 'commentsInput');
                commentsInput.setAttribute('placeholder', 'Input comments here: ');
                let sendButton=document.createElement('input');
                sendButton.setAttribute('type', 'button');
                sendButton.setAttribute('class', 'sendComments');
                sendButton.setAttribute('value', 'Send');
                sendButton.addEventListener('click', () => {
                    const commentValue=document.getElementsByClassName('commentsInput')[index].value;
                    //console.log(index);
                    //console.log(commentValue);
                    apiCall('job/comment', 'POST', {
                        id: jobID,
                        comment: commentValue,
                    });
                    commentsInput.value=null;
                    gotoWelcomeScreen();
                });
                commentsSendPart.appendChild(commentsInput);
                commentsSendPart.appendChild(sendButton);

                // see all liked users and all comments button
                let seeAllButtonPart = document.createElement('div');
                seeAllButtonPart.setAttribute('class', 'seeAllDetails');
                rightPart.appendChild(seeAllButtonPart);

                // liked users detail Space and hidden
                let likedSpace=document.createElement('div');
                likedSpace.setAttribute('class', 'likedSpace');
                rightPart.appendChild(likedSpace);
                for (let k=0; k<likeFeed.length; k++) {
                    let userLikesInfo = likeFeed[k];
                    // add all liked users space
                    let likesInfo = document.createElement('div');
                    likesInfo.setAttribute('class', 'likesInfo');
                    likesInfo.innerText=userLikesInfo.userName;
                    likesInfo.addEventListener('click', () => {
                        authUserID=userLikesInfo.userId;
                        gotoProfileScreen();
                    });
                    likedSpace.appendChild(likesInfo);
                }
                // comments Space and hidden
                let commentSpace=document.createElement('div');
                commentSpace.setAttribute('class', 'commentSpace');
                rightPart.appendChild(commentSpace);
                for (let j=0; j<commentsFeed.length; j++) {
                    let userInfo = commentsFeed[j];
                    // add all comments space
                    let commentInfo = document.createElement('div');
                    commentInfo.setAttribute('class', 'commentInfo');
                    commentInfo.innerText=userInfo.userName+': '+userInfo.comment;
                    commentInfo.addEventListener('click', () => {
                        authUserID=userInfo.userId;
                        gotoProfileScreen();
                    });
                    commentSpace.appendChild(commentInfo);
                }
                
                // show likes
                let showLikeButton=document.createElement('input');
                showLikeButton.setAttribute('type', 'button');
                showLikeButton.setAttribute('class', 'showLike');
                showLikeButton.setAttribute('value', 'Show Liked Users');
                showLikeButton.addEventListener('click', () => {
                    likedSpace.style.display='block';
                    commentSpace.style.display='none';
                    
                    showCommentsButton.style.display='block';
                    showLikeButton.style.display='none';

                    hideCommentsButton.style.display='none';
                    hideLikeButton.style.display='block';
                });

                //hide likes
                let hideLikeButton=document.createElement('input');
                hideLikeButton.setAttribute('type', 'button');
                hideLikeButton.setAttribute('class', 'hideLike');
                hideLikeButton.setAttribute('value', 'Hide Liked Users');
                hideLikeButton.addEventListener('click', () => {
                    likedSpace.style.display='none';
                    commentSpace.style.display='none';
                    
                    showCommentsButton.style.display='block';
                    showLikeButton.style.display='block';

                    hideCommentsButton.style.display='none';
                    hideLikeButton.style.display='none';
                });
                
                // show comments
                let showCommentsButton=document.createElement('input');
                showCommentsButton.setAttribute('type', 'button');
                showCommentsButton.setAttribute('class', 'showCommnets');
                showCommentsButton.setAttribute('value', 'Show All Comments');
                showCommentsButton.addEventListener('click', () => {
                    likedSpace.style.display='none';
                    commentSpace.style.display='block';
                    
                    showCommentsButton.style.display='none';
                    showLikeButton.style.display='block';

                    hideCommentsButton.style.display='block';
                    hideLikeButton.style.display='none';
                });

                // hidden comments button
                let hideCommentsButton=document.createElement('input');
                hideCommentsButton.setAttribute('type', 'button');
                hideCommentsButton.setAttribute('class', 'hideComments');
                hideCommentsButton.setAttribute('value', 'Hide All Comments');
                hideCommentsButton.addEventListener('click', () => {
                    likedSpace.style.display='none';
                    commentSpace.style.display='none';
                    
                    showCommentsButton.style.display='block';
                    showLikeButton.style.display='block';

                    hideCommentsButton.style.display='none';
                    hideLikeButton.style.display='none';
                });

                // initial button display
                likedSpace.style.display='none';
                commentSpace.style.display='none';
                hideLikeButton.style.display='none';
                hideCommentsButton.style.display='none';

                seeAllButtonPart.appendChild(showLikeButton);
                seeAllButtonPart.appendChild(hideLikeButton);
                seeAllButtonPart.appendChild(showCommentsButton);
                seeAllButtonPart.appendChild(hideCommentsButton);
            });
            
        };
    });
};

document.getElementById('btn-register').addEventListener('click', () => {
    const registerEmail = document.getElementById('register-email').value;
    const registerPassword = document.getElementById('register-password').value;
    const registerPasswordConfirm = document.getElementById('register-password-confirm').value;
    const registerName = document.getElementById('register-name').value;
    storePassword=registerPassword;
    storeEmail=registerEmail;
    if (registerEmail === "") {
        document.getElementById("error-message").textContent = "Input Email, please!";
		document.getElementById("error-popup").style.display = "block";
        return;
    }

    if (registerName === "") {
        document.getElementById("error-message").textContent = "Input Name, please!";
		document.getElementById("error-popup").style.display = "block";
        return;
    }

    if (registerPassword === "") {
        document.getElementById("error-message").textContent = "Input Password, please!";
		document.getElementById("error-popup").style.display = "block";
        return;
    }

    if (registerPassword !== registerPasswordConfirm) {
        document.getElementById("error-message").textContent = "Password don't match";
		document.getElementById("error-popup").style.display = "block";
        return;
    }

    register(registerEmail, registerPassword, registerName).then((body)=>{
        authToken = body.token;
        authUserID = body.userId;
        storeUserID = body.userId;
        gotoWelcomeScreen();
    });
});

document.getElementById('btn-login').addEventListener('click', () => {
    const loginEmail = document.getElementById('login-email').value;
    const loginPassword = document.getElementById('login-password').value;
    storePassword=loginPassword;
    storeEmail=loginEmail;
    login(loginEmail, loginPassword).then((body)=>{
        authToken = body.token;
        authUserID = body.userId;
        storeUserID = body.userId;
        //console.log(body);
        gotoWelcomeScreen();
    });
});

const gotoRegisterScreen = () => {
    document.getElementById('register-screen').style.display = 'block';
    document.getElementById('login-screen').style.display = 'none';
    document.getElementById('feed-screen').style.display = 'none';
    document.getElementById('profile-screen').style.display = 'none';
    document.getElementById('user-info-update-screen').style.display = 'none'; 
    document.getElementById('job-add-screen').style.display = 'none'; 
    document.getElementById('job-update-screen').style.display = 'none';

    document.getElementById('profile-leave-btn').style.display = 'none';
    document.getElementById('profile-btn').style.display = 'none';
    document.getElementById('logout-btn').style.display = 'none';
    document.getElementById('be-watchee-btn').style.display = 'none';
};

const gotoLoginScreen = () => {
    document.getElementById('login-screen').style.display = 'block';
    document.getElementById('register-screen').style.display = 'none';
    document.getElementById('feed-screen').style.display = 'none';
    document.getElementById('profile-screen').style.display = 'none'; 
    document.getElementById('user-info-update-screen').style.display = 'none';
    document.getElementById('job-add-screen').style.display = 'none';
    document.getElementById('job-update-screen').style.display = 'none';  
    
    document.getElementById('profile-leave-btn').style.display = 'none';
    document.getElementById('profile-btn').style.display = 'none';
    document.getElementById('logout-btn').style.display = 'none';
    document.getElementById('be-watchee-btn').style.display = 'none';
};

const closeErrorPopup = () => {
    document.getElementById("error-popup").style.display = "none";
};

const gotoWelcomeScreen = () => {
    //console.log(storeUserID);
    document.getElementById('feed-screen').innerHTML='';

    document.getElementById('feed-screen').style.display = 'block';
    document.getElementById('register-screen').style.display = 'none';
    document.getElementById('login-screen').style.display = 'none';
    document.getElementById('profile-screen').style.display = 'none';
    document.getElementById('user-info-update-screen').style.display = 'none';
    document.getElementById('job-add-screen').style.display = 'none'; 
    document.getElementById('job-update-screen').style.display = 'none';   
    
    document.getElementById('profile-btn').style.display = 'block';
    document.getElementById('profile-leave-btn').style.display = 'none';
    document.getElementById('logout-btn').style.display = 'none';
    document.getElementById('be-watchee-btn').style.display = 'block';

    const queryString = window.location.search;
    const urlParams = new URLSearchParams(queryString);
    let startIndex = urlParams.get('start')
    if (startIndex == null) {
        startIndex = 0;
    }
    getJobList(startIndex);
};

const gotoProfileScreen = () => {
    document.getElementById('job-list').innerHTML='';
    document.getElementById('watched-users').innerHTML='';

    document.getElementById('profile-screen').style.display = 'block';
    document.getElementById('feed-screen').style.display = 'none';
    document.getElementById('register-screen').style.display = 'none';
    document.getElementById('login-screen').style.display = 'none';
    document.getElementById('user-info-update-screen').style.display = 'none';
    document.getElementById('job-add-screen').style.display = 'none';
    document.getElementById('job-update-screen').style.display = 'none';   
    
    document.getElementById('profile-leave-btn').style.display = 'block';
    document.getElementById('profile-btn').style.display = 'none';
    document.getElementById('logout-btn').style.display = 'block';
    document.getElementById('be-watchee-btn').style.display = 'none';

    if (authUserID === storeUserID) {
        document.getElementById('user-detail-edit').style.display = 'block';
        document.getElementById('user-add-job').style.display = 'block';
        document.getElementById('user-follow').style.display = 'none';
        document.getElementById('user-unfollow').style.display = 'none';
    } else {
        getProfile(authUserID).then(body => {
            let watcheeList=body.watcheeUserIds;
            //console.log(watcheeList);
            if (watcheeList.includes(storeUserID)){
                document.getElementById('user-unfollow').style.display = 'block';
                document.getElementById('user-follow').style.display = 'none';
            } else {
                document.getElementById('user-follow').style.display = 'block';
                document.getElementById('user-unfollow').style.display = 'none';
            }
        });
        document.getElementById('user-detail-edit').style.display = 'none';
        document.getElementById('user-add-job').style.display = 'none';
    }
    
    getProfile(authUserID).then(body => {
        //console.log(body);
        let userName = body.name ? body.name : '';
        let userImage=body.image ? body.image : '';
        let userEmail=body.email ? body.email : '';
        let watchees=body.watcheeUserIds.length;
        let jobs=body.jobs;
        
        authEmail=userEmail;
        authName=userName;
        storeImage=userImage;
        authImage=userImage;
        
        document.getElementById('unwatch-user').addEventListener('click', () => {
            apiCall('user/watch', 'PUT', {
                email: userEmail,
                turnon: false
            });
        });
        document.getElementById('watch-user').addEventListener('click', () => {
            apiCall('user/watch', 'PUT', {
                email: userEmail,
                turnon: true
            });
        });
        document.getElementById('user-name-info').innerText=' '+userName;
        document.getElementById('user-email-info').innerText=' '+userEmail;
        document.getElementById('user-image-info').src=userImage;
        document.getElementById('watch-count').innerText=watchees;
        
        for (let i=0; i<jobs.length; i++) {
            let job = jobs[i];
            let title = job.title;
            let img = job.image;
            let start = new Date(job.start);
            start = start.getDate() + '/' + (start.getMonth() + 1) + '/' + start.getFullYear();
            let description = job.description;
            let postTime = formatTime(job.createdAt);
            let likesAmount=job.likes.length;
            let commentsAmount=job.comments.length;
            let jobId=job.id;

            // create job detail container
            let jobCard = document.createElement('div');
            jobCard.setAttribute('id', 'jobContainer');
            document.getElementById('job-list').appendChild(jobCard);

            let titleCard= document.createElement('h1');
            titleCard.setAttribute('id', 'titleCard');
            titleCard.innerText=title;
            jobCard.appendChild(titleCard);
            
            let postCard=document.createElement('h5');
            postCard.setAttribute('id', 'postCard');
            postCard.innerText='Create At: '+postTime;
            jobCard.appendChild(postCard);

            let imgCard= document.createElement('img');
            imgCard.setAttribute('id', 'imgCard');
            imgCard.src = img;
            jobCard.appendChild(imgCard);

            let descriptionCard=document.createElement('p');
            descriptionCard.setAttribute('id', 'descriptionCard');
            descriptionCard.innerText=description;
            jobCard.appendChild(descriptionCard);

            let startCard=document.createElement('h5');
            startCard.setAttribute('id', 'startCard');
            startCard.innerText='Start At: '+start;
            jobCard.appendChild(startCard);

            let LikesCard=document.createElement('h5');
            LikesCard.setAttribute('id', 'likesCard');
            LikesCard.innerText='Likes: '+likesAmount;
            jobCard.appendChild(LikesCard);

            let CommentsCard=document.createElement('h5');
            CommentsCard.setAttribute('id', 'commentsCard');
            CommentsCard.innerText='Comments: '+commentsAmount;
            jobCard.appendChild(CommentsCard);

            if (authUserID === storeUserID){
                let editJobButton=document.createElement('input');
                editJobButton.setAttribute('id', 'editJobButton');
                editJobButton.setAttribute('type', 'button');
                editJobButton.setAttribute('value', 'Edit Job');
                editJobButton.addEventListener('click', () => {
                    storeJobId=jobId;
                    storeJobImage=img;
                    storeJobTitle=title;
                    storeJobStart=job.start;
                    storeJobDescription=description;
                    gotoJobUpdateScreen();
                });
                jobCard.appendChild(editJobButton);

                let deleteJobButton=document.createElement('input');
                deleteJobButton.setAttribute('id', 'deleteJobButton');
                deleteJobButton.setAttribute('type', 'button');
                deleteJobButton.setAttribute('value', 'Detele Job');
                deleteJobButton.addEventListener('click', () => {
                    apiCall('job', 'DELETE', {
                        id: jobId
                    })
                    gotoProfileScreen();
                });
                jobCard.appendChild(deleteJobButton);
            }
        }
        for(let j=0; j<body.watcheeUserIds.length; j++) {
            let id=body.watcheeUserIds[j];
            getProfile(id).then(data => {
                let name=data.name;
                let nameSpace=document.createElement('p');
                nameSpace.setAttribute('class', 'namePut');
                nameSpace.innerText=name;
                nameSpace.addEventListener('click', () => {
                    authUserID = id;
                    gotoProfileScreen();
                } );
                document.getElementById('watched-users').appendChild(nameSpace);
            });
        } 
        
    }); 
    
};

const gotoInfoUpdateScreen = () => {
    document.getElementById('user-info-update-screen').style.display = 'block'; 
    document.getElementById('feed-screen').style.display = 'none';
    document.getElementById('register-screen').style.display = 'none';
    document.getElementById('login-screen').style.display = 'none';
    document.getElementById('profile-screen').style.display = 'none';
    document.getElementById('job-add-screen').style.display = 'none'; 
    document.getElementById('job-update-screen').style.display = 'none'; 
    
    document.getElementById('profile-btn').style.display = 'none';
    document.getElementById('profile-leave-btn').style.display = 'none';
    document.getElementById('logout-btn').style.display = 'none';
    document.getElementById('be-watchee-btn').style.display = 'none';
};

const gotoJobAddScreen = () => {
    document.getElementById('job-add-screen').style.display = 'block'; 
    document.getElementById('user-info-update-screen').style.display = 'none'; 
    document.getElementById('feed-screen').style.display = 'none';
    document.getElementById('register-screen').style.display = 'none';
    document.getElementById('login-screen').style.display = 'none';
    document.getElementById('profile-screen').style.display = 'none';
    document.getElementById('job-update-screen').style.display = 'none';
     
    document.getElementById('profile-btn').style.display = 'none';
    document.getElementById('profile-leave-btn').style.display = 'none';
    document.getElementById('logout-btn').style.display = 'none';
    document.getElementById('be-watchee-btn').style.display = 'none';
};

const gotoJobUpdateScreen = () => {
    document.getElementById('job-add-screen').style.display = 'none'; 
    document.getElementById('user-info-update-screen').style.display = 'none'; 
    document.getElementById('feed-screen').style.display = 'none';
    document.getElementById('register-screen').style.display = 'none';
    document.getElementById('login-screen').style.display = 'none';
    document.getElementById('profile-screen').style.display = 'none';
    document.getElementById('job-update-screen').style.display = 'block';
     
    document.getElementById('profile-btn').style.display = 'none';
    document.getElementById('profile-leave-btn').style.display = 'none';
    document.getElementById('logout-btn').style.display = 'none';
    document.getElementById('be-watchee-btn').style.display = 'none';
};

const saveInfoUpdate = () => {
    let newEmail = document.getElementById('update-email').value;
    let newName = document.getElementById('update-name').value;
    let newPassword = document.getElementById('update-password').value; 
    apiCall('user', 'PUT', {
        email: newEmail === "" ? authEmail : newEmail,
        password: newPassword === "" ? storePassword : newPassword,
        name: newName === "" ? authName : newName,
        image: authImage === "" ? storeImage : authImage
    });
    if(newPassword !== "") {
        storePassword = newPassword;
    }
    document.getElementById('update-email').value=null;
    document.getElementById('update-name').value=null;
    document.getElementById('update-password').value=null;
    document.getElementById("new-pic").value=null;
    gotoProfileScreen();
};

const saveJobAdd = () => {
    let jobTitle = document.getElementById('job-title-input').value;
    if (jobTitle === "") {
        document.getElementById("error-message").textContent = "Please input title";
		document.getElementById("error-popup").style.display = "block";
        return;
    } 
    let jobStartInput=document.getElementById('job-start-time').value;
    if (jobStartInput === "") {
        document.getElementById("error-message").textContent = "Please input start datetime";
		document.getElementById("error-popup").style.display = "block";
        return;
    } 
    let jobStartTime = new Date(jobStartInput);
    jobStartTime=jobStartTime.toISOString();
    let jobDescription=document.getElementById('job-description').value;
    if (jobDescription === "") {
        document.getElementById("error-message").textContent = "Please input job description";
		document.getElementById("error-popup").style.display = "block";
        return;
    }
    apiCall('job', 'POST', {
        title: jobTitle,
        image: jobImage,
        start: jobStartTime,
        description: jobDescription
    });
    document.getElementById('job-title-input').value=null;
    document.getElementById('job-description').value=null;
    document.getElementById("job-pic").value=null;
    document.getElementById('job-start-time').value=null;
    gotoProfileScreen();
};

const updateJob = () => {
    let newjobTitle = document.getElementById('new-job-title-input').value;
    let newJobStartInput=document.getElementById('new-job-start-time').value;
    let newJobStartTime ="";
    if (newJobStartInput !== "") {
        newJobStartTime = new Date(newJobStartInput);
        newJobStartTime=newJobStartTime.toISOString();
    } 
    let newJobDescription=document.getElementById('new-job-description').value;
    apiCall('job', 'PUT', {
        id: storeJobId,
        title: newjobTitle === "" ? storeJobTitle : newjobTitle,
        image: newJobImage === "" ? storeJobImage : newJobImage,
        start: newJobStartInput === "" ? storeJobStart : newJobStartTime,
        description: newJobDescription === "" ? storeJobDescription : newJobDescription
    });
    document.getElementById('new-job-title-input').value=null;
    document.getElementById('new-job-description').value=null;
    document.getElementById("new-job-pic").value=null;
    document.getElementById('new-job-start-time').value="";
    gotoProfileScreen();
};

const readFileForJobAdd = () => {
    let file = document.getElementById('job-pic').files[0];
    if (file) {
        let reader= new FileReader();
        reader.readAsDataURL(file);
        reader.onload=function(e) {
            jobImage=reader.result;
            return;
        }
    }
}

const readFileForUpdateAdd = () => {
    let file = document.getElementById('new-job-pic').files[0];
    if (file) {
        let reader= new FileReader();
        reader.readAsDataURL(file);
        reader.onload=function(e) {
            newJobImage=reader.result;
            return;
        }
    }
}

const readFileForInfoUpadte = () => {
    let file=document.getElementById("new-pic").files[0];
    if (file) {
        let reader= new FileReader();
        reader.readAsDataURL(file);
        reader.onload=function(e) {
            authImage=reader.result;
            return;
        }
    }
}

const closeProfile = () => {  
    gotoWelcomeScreen();
    authUserID = storeUserID;
};

const openInputEmail = () => {
    document.getElementById('be-watchee-popup').style.display = 'block';
}

const closeInputEmail = () => {
    document.getElementById('be-watchee-popup').style.display = 'none';
    document.getElementById('email-input-to-be-watchee').value=null;
}

const addEmailTobeWatchee = () => {
    let email=document.getElementById('email-input-to-be-watchee').value;
    if(email==="") {
        document.getElementById("error-message").textContent = "Please input email";
		document.getElementById("error-popup").style.display = "block";
        document.getElementById("be-watchee-popup").style.display = "none";
        return;
    }
    if(email===storeEmail) {
        document.getElementById("error-message").textContent = "You can not be your watchee";
		document.getElementById("error-popup").style.display = "block";
        document.getElementById("be-watchee-popup").style.display = "none";
        document.getElementById('email-input-to-be-watchee').value=null;
        return;
    }
    apiCall('user/watch', 'PUT', {
        email: email,
        turnon: true
    })
    document.getElementById('email-input-to-be-watchee').value=null;
    closeInputEmail();
    gotoWelcomeScreen();
}

document.getElementById('btn-goto-register').addEventListener('click', gotoRegisterScreen);
document.getElementById('btn-goto-login').addEventListener('click', gotoLoginScreen);
document.getElementById('errorClose').addEventListener('click', closeErrorPopup);
document.getElementById('btn-profile').addEventListener('click', gotoProfileScreen);
document.getElementById('btn-profile-leave').addEventListener('click', closeProfile);
document.getElementById('edit-info').addEventListener('click', gotoInfoUpdateScreen);
document.getElementById('btn-cancel').addEventListener('click', gotoProfileScreen);
document.getElementById('btn-save').addEventListener('click', saveInfoUpdate);
document.getElementById("new-pic").addEventListener("change", readFileForInfoUpadte);
document.getElementById("be-watchee-btn").addEventListener("click", openInputEmail);
document.getElementById('be-watchee-close').addEventListener('click', closeInputEmail);
document.getElementById('be-watchee-add').addEventListener('click', addEmailTobeWatchee);
document.getElementById('btn-job-add').addEventListener('click', saveJobAdd);
document.getElementById('user-add-job').addEventListener('click', gotoJobAddScreen);
document.getElementById('btn-job-add-cancel').addEventListener('click', gotoProfileScreen);
document.getElementById("job-pic").addEventListener("change", readFileForJobAdd);
document.getElementById('btn-job-update-cancel').addEventListener('click', gotoProfileScreen);
document.getElementById('btn-job-update').addEventListener('click', updateJob);
document.getElementById("new-job-pic").addEventListener("change", readFileForUpdateAdd);
document.getElementById("btn-logout").addEventListener("click", gotoLoginScreen);
