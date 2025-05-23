
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    console.log(cookieValue)
    return cookieValue;
}
const csrftoken = getCookie('csrftoken');

async function find_open_restaurants(){

    let selected_value = ""
    const radioButtons = document.querySelectorAll('input[type="radio"][name="choice"]');
    radioButtons.forEach(radio => {

    if (radio.checked) {
        selected_value = radio.value
        }
    });


    let timestamp =""
    if (selected_value  == ""){
        alert("Make a valid selection!")
        return
    } else if (selected_value == "current_time"){
        timestamp = Math.floor(Date.now() / 1000);
    } else if (selected_value == "user_input"){
        const inputText = document.getElementById("userInput").value;
        timestamp = inputText
    }
    var endpoint = `search?timestamp=${timestamp}`
    const result = await httpRequest(endpoint, 'GET', null)


    if(result == null){
        return
    }
    const open_restaurants_div = document.querySelector("#open-restaurants")
    open_restaurants_div.innerHTML=""
    const open_restaurants_ul = document.createElement('ul')
    open_restaurants_div.appendChild(open_restaurants_ul)
    if (result.total == "0"){
        const list_item = document.createElement('li')
        list_item.className = "no-open-restaurants"
        list_item.textContent = "Sorry, there aren’t any open restaurants right now."
        open_restaurants_ul.appendChild(list_item)
        open_restaurants_div.appendChild(open_restaurants_ul)
        return
    }
    open_restaurants_div.innerHTML = ""
    result.open_restaurants.forEach(item=>{
        const list_item = document.createElement('li')
        list_item.textContent = item
        open_restaurants_ul.appendChild(list_item)
    })
    open_restaurants_div.appendChild(open_restaurants_ul)
}

async function httpRequest(urlEndpoint, method, payload){
     var baseURL = `http://127.0.0.1:8000/home/restaurantfinder`
     var endpoint = urlEndpoint
     var url = `${baseURL}/${endpoint}`

     const request = new Request(url,
        {
            method: method,
            headers: {'X-CSRFToken': csrftoken2},
            mode: 'same-origin',
            body: payload
        }
    );

    const test = await fetch(request)
    .then((response)=>{
        if(!response.ok){

            throw new Error(`Unexpected error occured. HTTP Status: ${response.status}`);
        }

        return response.json()
    })
    .then(data=>{
        if(method == 'GET'){
            return data
        }
    })
    .catch((error)=>{
        alert(error)
        return null
    });

    return test
}

function updateClock() {
    const now = new Date();
    const hours = String(now.getHours()).padStart(2, '0');
    const minutes = String(now.getMinutes()).padStart(2, '0');
    const seconds = String(now.getSeconds()).padStart(2, '0');
    document.querySelector('#clock').innerText = `${hours}:${minutes}:${seconds}`;
}

setInterval(updateClock, 1000);
updateClock();