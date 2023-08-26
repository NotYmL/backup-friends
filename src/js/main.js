let token;

function htmlEscape(text) {
    return text.replace(/&/g, '&amp;').
        replace(/</g, '&lt;').  // it's not neccessary to escape >
        replace(/"/g, '&quot;').
        replace(/'/g, '&#039;');
}

let inpTag = document.getElementById("file1");
let buttonTag = document.getElementById("loginButton");

function openFileOption(){ inpTag.click(); }

buttonTag.onclick = function (event) {
    let file = inpTag.files[0];
    
    if (file) {
        let reader = new FileReader();

        reader.onload = function (event) {
            let fileContent = event.target.result;
            try {
                let jsonData = JSON.parse(fileContent);
                list(jsonData);
            } catch (error) {
                console.error("Error parsing JSON:", error);
            }
        };

        reader.readAsText(file, 'UTF-8');
    } else {
        console.log("No file selected.");
    }
}

function list(x) {
    // hide upload box
    document.getElementsByClassName("mainBox")[0].style.display = "none"

    // list users
    for(let i=0; i<x.length; i++) {
        let displayName = x[i]['user']['username'];
        let userID = x[i]['id']
        let username = x[i]['user']['global_name'];
        let avatar = "https://cdn.discordapp.com/avatars/"+userID+"/"+x[i]['user']['avatar']+".webp?size=64"
        
        if(username == null) {
            username = displayName + "#" + x[i]['user']['discriminator'];
        }

        if(x[i]['user']['avatar'] == null){
            avatar = "pfp.webp"
        }

        if(x[i]['user']['discriminator'] == 0){
            username = displayName
        }

        if(displayName.length > 10) 
            displayName = displayName.substr(0, 10)+'...';
        
        if(username.length > 15) 
            username = username.substr(0, 10)+'...';

        //sanitize data
        username = htmlEscape(username);
        displayName = htmlEscape(displayName);
        
        // add to dom
        document.getElementsByClassName("container")[0].innerHTML += `
            <div class="border">
                <div class="box">
                    <div class="img">
                        <img src="${avatar}" alt="pfp" width="64" height="64">
                    </div>
                    <div class="username">
                        <h1>${displayName}</h1>
                        <h2 class="mt-0">${username}</h2>
                    </div>
                    <div class="send-Button-Wrapper">
                        <button class="button" userID="${userID}" >Send</button>
                    </div>
                </div>
            </div>
        `
    }
    
    document.querySelectorAll("button").forEach((button) => {
        button.onclick = function (event) {
            fetch("/add/"+button.getAttribute("userID"));
        }
    })
}