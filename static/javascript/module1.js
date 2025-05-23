
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

    const timestamp_in_sec = 1747666860// Math.floor(Date.now() / 1000);
    const open_restaurants_list = document.querySelector("#open-restaurants-list")
    var endpoint = `search?timestamp=${timestamp_in_sec}`
    const result = await httpRequest(endpoint, 'GET', null)
    console.log(result)
    result.open_restaurants.forEach(item=>{
        console.log(item)
        const list_item = document.createElement('li')
        list_item.textContent = item
        open_restaurants_list.appendChild(list_item)
    })
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
            return Promise.reject(response)
        }

        return response.json()
    })
    .then(data=>{
        if(method == 'GET'){
            return data
        }
    })
    .catch((error)=>{
        console.log("error")
    });

    return test
}
