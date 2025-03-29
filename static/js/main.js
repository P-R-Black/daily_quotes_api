const body = document.querySelector('body')
const toggle = body.querySelector('.toggle')
const modeSwitch = body.querySelectorAll('.toggle-switch')
const nav = body.querySelector('nav')
const modeText = body.querySelector('.mode-text')
// const navLogoText = body.querySelector('.logo-text')

//const mobileMoon = body.querySelector('.mobile-moon')
//const mobileSun = body.querySelector('.mobile-sun')
//const mobileSearchBox = body.querySelector('.mobile-search-box')
//const mobileSearchIcon = body.querySelector('#mobile-search-icon')


// Star maker
let starIndex = 0
const newStarMaker = () => {
    let starCount = 500;
    let scene = body.querySelector(".hero_container");

    while (starIndex <= starCount){
        let star = document.createElement('div');
        let x = Math.floor(Math.random() * window.innerWidth);
        let y = Math.floor(Math.random() * window.innerHeight);
        let size = Math.random() * 2;

        star.classList.add('starScene');
        star.style.left = x + 'px';
        star.style.top = y + 'px';
        star.style.width = 1 + size + 'px';
        star.style.height = 1 + size + 'px';

        // Adding flickering animation with random delay and duration
        let duration = (Math.random() * 4 + 1).toFixed(2) + "s"; // Between 1s - 5s
        let delay = (Math.random() * 10).toFixed(2) + "s"; // Between 0s - 10s
        star.style.animation = `flicker ${duration} infinite alternate`;
        star.style.animationDelay = delay;

        scene.appendChild(star)
         starIndex += 1;
    }
}


// Dark mode and light mode
const darkLightModeToggle = () => {
    modeSwitch.forEach((modes) => {
        modes.addEventListener('click', () => {

            body.classList.toggle('dark')
            nav.classList.toggle('dark')

        if (body.classList.contains("dark")) {
            localStorage.setItem('darkMode', 'enabled');
             newStarMaker();

        } else {
            localStorage.setItem('darkMode', 'disabled'); // Save preference
            removeStars()
            starIndex = 0
        }

        })
    })
}




const removeStars = () => {
    console.log('removeStars called')
    document.querySelectorAll('.starScene').forEach(star => star.remove())
}


darkLightModeToggle()

// Check localStorage for saved mode preference
const savedMode = localStorage.getItem('darkMode');
if (savedMode === 'enabled') {
    body.classList.add('dark');
    nav.classList.add('dark');
    newStarMaker();

}  else {
     body.classList.remove('dark');
     nav.classList.remove('dark');

}


if (!localStorage.getItem('darkMode')) {
    if (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) {
        body.classList.add('dark');
        nav.classList.add('dark');
        localStorage.setItem('darkMode', 'enabled');
        newStarMaker();
    }
}

/// picture layout
let picStyleButton = document.querySelectorAll('.picStyleButton')
let pictureBox = document.getElementById('picture_box')
let picStyle = ""
picStyleButton.forEach((pic) => {
    pic.addEventListener('click', (event)=> {
        event.preventDefault()
        picStyle = pic.value
        adjustQuoteBox(picStyle)

        if (picStyle === "Instagram"){
            pictureBox.style.width = '360px'; // 1080
            pictureBox.style.height = '360px'; // 1080
        }

        if (picStyle === "TikTok"){
            pictureBox.style.width = '275px'; // 1080
            pictureBox.style.height = '425px'; //1920
        }
    })
});


let backgroundColorButtons = document.querySelectorAll('.bgColorButton')
let buttonColor;
let backgroundColor = "#ffffff";

backgroundColorButtons.forEach((bgButton) => {
    bgButton.addEventListener('click', (event) => {
        event.preventDefault()
        buttonColor = bgButton.getAttribute("id")

        switch(buttonColor){
            case "whiteButton":
                backgroundColor = "#ffffff"
                break;
            case "blackButton":
                backgroundColor = "#000000"
                break;
            case "redButton":
                backgroundColor = "#FF0000"
                break;
            case "blueButton":
                backgroundColor = "#0509f7"
                break;
            case "greenButton":
                backgroundColor = "#05f74a"
                break;
            case "orangeButton":
                backgroundColor = "#f7a605"
                break;
            case "yellowButton":
                backgroundColor = "#f7eb05"
                break;
            case "violetButton":
                backgroundColor = "#ef05f7"
                break;
            case "grayButton":
                backgroundColor = "#7F7F7F"
                break;
            case "lightBlackButton":
                backgroundColor = "#5C5454"
                break;
            case "pinkButton":
                backgroundColor = "#FF83B2"
                break;
            case "lightBlueButton":
                backgroundColor = "#93B0F5"
                break;
            case "darkGreenButton":
                backgroundColor = "#7D8682"
                break;
            case "darkPurpleButton":
                backgroundColor = "#573C0E"
                break;
            case "tealButton":
                backgroundColor = "#10B9A8"
                break;
            case "darkBlueButton":
                backgroundColor = "#5229C4"
                break;
            case "darkerGreenButton":
                backgroundColor = "#3A6D45"
                break;
            default:
                backgroundColor = "#FF0000"
        }
        pictureBox.style.background = backgroundColor;
    })
})


// get font color
let fontColorButtons = document.querySelectorAll('.fontColorButton')
let fontButtonColor;
let fontColor = "#000000";

fontColorButtons.forEach((fontButton) => {
    fontButton.addEventListener('click', (event) => {
        event.preventDefault()
        buttonColor = fontButton.getAttribute("id")

        switch(buttonColor){
            case "whiteFontButton":
                fontColor = "#ffffff"
                break;
            case "blackFontButton":
                fontColor = "#000000"
                break;
            case "redFontButton":
                fontColor = "#FF0000"
                break;
            case "blueFontButton":
                fontColor = "#0509f7"
                break;
            case "greenFontButton":
                fontColor = "#05f74a"
                break;
            case "orangeFontButton":
                fontColor = "#f7a605"
                break;
            case "yellowFontButton":
                fontColor = "#f7eb05"
                break;
            case "violetFontButton":
                fontColor = "#ef05f7"
                break;
            default:
                fontColor = "#000000"
        }
        pictureBox.style.color = fontColor;
    })
})



// choose shadow option
const pictureQuote = document.getElementById('picture_quote');
const pictureAuthor = document.getElementById('picture_author')
let shadowButton = document.querySelectorAll('.shadowButton');
let shadowButtonColor;
let shadowFont = "0px 0px 0px rgba(0, 0, 0, 0)"


shadowButton.forEach((shadow) => {
shadow.addEventListener('click', (event) => {
    event.preventDefault()
    shadowButtonColor = shadow.getAttribute("id")

    switch(shadowButtonColor){
        case "littleShadowButton":
            shadowFont = "0px 0.5px 1px rgba(0, 0, 0, 0.25)"
            break;
        case "mediumShadowButton":
            shadowFont = "1px 1px 1px rgba(0, 0, 0, 0.50)"
            break;
        case "largeShadowButton":
            shadowFont = "2px 2px 4px rgba(0, 0, 0, 0.50)"
            break;
        default:
            shadowFont = "0px 0px 0px rgba(0, 0, 0, 0)"

        }
        pictureQuote.style.textShadow = shadowFont;
        pictureAuthor.style.textShadow = shadowFont;
    })
})


// place quote text on canvas
const quote = document.querySelector('.quote')
const quoteAuthor = document.querySelector('.author')
const quoteInPic = document.getElementById('quote_in_pic')
const authorInPic = document.getElementById('author_in_pic')

const adjustQuoteBox = (currPicStyle) => {
    if(currPicStyle === "Instagram"){
     quoteInPic.style.marginTop = "-10px"
        quoteInPic.style.width = "340px";
        quoteInPic.style.height = "280px";
        // quoteInPic.style.border = '1px solid red';

        authorInPic.style.width = '340px'
        authorInPic.style.height = '32px'
        // authorInPic.style.border = '1px solid blue'

        adjustQuoteSize(quote, quoteInPic.style.width, quoteInPic.style.height, quoteAuthor, authorInPic.style.width, authorInPic.style.height)

    }

     if(currPicStyle === "TikTok"){
        quoteInPic.style.width = "260px";
        quoteInPic.style.height = "340px";
        quoteInPic.style.marginTop = "-35px"
        // quoteInPic.style.border = '1px solid red';

        authorInPic.style.width = '260px';
        authorInPic.style.height = '32px';
        // authorInPic.style.border = '1px solid blue'

        adjustQuoteSize(quote, quoteInPic.style.width, quoteInPic.style.height, quoteAuthor, authorInPic.style.width, authorInPic.style.height)

    }
}


const adjustQuoteSize = (quote, boxWidth, boxHeight, quoteAuthor, authorBoxWidth, authorBoxHeight) => {

    // Adjust quote size
    let styles = window.getComputedStyle(quote, null)
    let quoteFont = styles.getPropertyValue('font-size')

    pictureQuote.style.fontSize = "32px";
    pictureQuote.innerHTML = quote.innerHTML

    let boxHeightNumber =  parseInt(boxHeight.split('px')[0])
    let newFontSize = parseInt(quoteFont.split('px')[0]);

    while (pictureQuote.offsetHeight > boxHeightNumber ){
        newFontSize -= 1
        pictureQuote.style.fontSize = `${newFontSize}px`;
        pictureQuote.innerHTML = quote.innerHTML;
    }



    // Adjust author name size
    let authorStyles = window.getComputedStyle(quoteAuthor, null);
    let authorFont = authorStyles.getPropertyValue('font-size');

    pictureAuthor.style.fontSize = "32px";
    pictureAuthor.innerHTML = quoteAuthor.innerHTML

    let authorBoxHeightNumber =  parseInt(authorBoxHeight.split('px')[0])
    let authorNewFontSize = parseInt(authorFont.split('px')[0]);

     while (pictureAuthor.offsetHeight > authorBoxHeightNumber ){
        authorNewFontSize -= .05
        pictureAuthor.style.fontSize = `${authorNewFontSize}px`;
        pictureAuthor.innerHTML = quoteAuthor.innerHTML;
    }
}



// tag options dropdown
var expandButton = document.getElementById('expandButton');
var hiddenTagContainer = document.querySelector('.hidden_tags_container')

expandButton.addEventListener('click', (e) => {
    e.preventDefault();
    hiddenTagContainer.classList.toggle('show');
});



document.addEventListener('DOMContentLoaded', function() {
    // Function to handle tag selection
    function handleTagSelection(event) {
        event.preventDefault();  // Prevent page refresh

        const selectedValue = this.value;
        console.log('selectedValue', selectedValue)

        fetch(window.location.pathname + `?selected_value=${encodeURIComponent(selectedValue)}`, {
            method: 'GET',
            headers: {
                'X-Requested-With': 'XMLHttpRequest'
            }
        })
        .then(response => response.json())
        .then(data => {
            console.log('Selected:', selectedValue);

            const messageBox = document.getElementById('messageBox');
            if (messageBox) {
                messageBox.innerHTML = `${selectedValue}`;
            }

            // Close the hidden tag container after selection
            if(hiddenTagContainer.classList.contains('show')){
                hiddenTagContainer.classList.remove('show')
            }
        })
        .catch((error) => {
            console.error('Error:', error);
        });
    }

    // Attach event listeners for both sets of buttons (even hidden ones)
    const selectButtons = document.querySelectorAll('.tags_container .select_button, .secondary_tags_container, .tag_button, .more_options_button');
    const secondQuoteButton = document.querySelector('.second_quote_button')

    selectButtons.forEach(button => {
        button.addEventListener('click', handleTagSelection);
    });

    secondQuoteButton.addEventListener('click', (e) => {
        e.preventDefault()

    })

    // Handle "Get Quote" button as normal form submission
    const getQuoteButton = document.querySelector('.get_quote_form .select_button');
    getQuoteButton.addEventListener('click', function() {
        document.querySelector('.get_quote_form').submit();
    });
});



// download button
let downloadButton = document.getElementById('download-button')
let pictureBoxQuote = document.getElementById('')

downloadButton.addEventListener('click', (e) => {
    e.preventDefault()

    console.log('picStyle inside download', picStyle)
    console.log('backgroundColor inside download', backgroundColor)
    console.log('fontcolor inside download', fontColor)
    console.log('quoteInPic inside download', quoteInPic.innerText)
    console.log('authorInPic inside download', authorInPic.innerText)

    let imageStyle = picStyle
    let imageBG = backgroundColor
    let imageFontColor = fontColor
    let imageQuote = quoteInPic.innerText
    let imageAuthor = authorInPic.innerText


    // send data  to the backend using AJAX
    $.ajax({
        url: "/download-image/",
        method : "POST",
        headers: {"X-Requested-With": "XMLHttpRequest",'X-CSRFToken': getCookie("csrftoken")},
        data: {
            'image_style': imageStyle,
            'background_color': imageBG,
            'font_color': imageFontColor,
            'quote':imageQuote,
            'author':imageAuthor,
            'shadow': shadowFont,
        },

        mode: 'same-origin', // Do not send CSRF token to another domain.
        csrfmiddlewaretoken: '{% csrf_token %}',
        xhrFields:{responseType: 'blob' },
        success: function (response) {
            let blob = new Blob([response], { type: "image/png" });  // Correct Blob creation
            let link = document.createElement('a');
            link.href = URL.createObjectURL(blob); // Create a valid object URL
            link.download = 'daily_quote.png';
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link); // Cleanup the DOM
        },
        error: function (xhr, status, error) {
            console.log("Error downloading image:", error);
        }
    });
});


const getCookie = (name) => {
    let cookieValue = null;
    if(document.cookie && document.cookie !== "") {
        const cookies = document.cookie.split(";");
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string being with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + "=")) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
