

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



async function newPost(){
    const post_msg = document.querySelector("#post");
    const value = post_msg.value
    const payloadData = {data: value}
    const payload = JSON.stringify(payloadData)

    var endpointURL = 'home/post/new'
    httpRequest(endpointURL, 'POST', payload)
    setTimeout(()=>{
        location.reload(true)
        console.log(event);
        }, 500)

}

async function reply(element, event){
    var el = event.target.id

}

async function httpRequest(urlEndpoint, method, payload){
     var baseURL = `http://127.0.0.1:8000`
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

    fetch(request)
    .then((response)=>{
        if(!response.ok){
            return Promise.reject(response)
        }
        if(response.ok){
            return response
        }

    })
    .then((response)=>{
        console.log(response)
        const data = response.text()
        if(method == 'GET'){
        console.log(data)
            return data
        }

    })
    .catch((error)=>{
        console.log("error")
    });

}
