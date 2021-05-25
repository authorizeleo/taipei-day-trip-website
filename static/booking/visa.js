const order_Btn = document.querySelector('.order-Btn')
const error_tip = document.querySelector('#error_tip')
const orders_name = document.getElementById('booking_name')
const orders_email = document.getElementById('booking_email')
const orders_phone = document.getElementById('booking_tel')
TPDirect.setupSDK(20401, 'app_ocU0IgjFiSM2bEh7YK2ksSEvAZAcshizGojpuWUcYyD6XtcvyXhgbyieDVzR', 'sandbox')

var fields = {
    number: {
        element: '#booking_card',
        placeholder: '**** **** **** ****'
    },
    expirationDate: {
        element: '#booking_time',
        placeholder: 'MM / YY'
    },
    ccv: {
        element: '#booking_vaild',
        placeholder: '後三碼'
    }
}

TPDirect.card.setup({
    fields: fields,
    styles: {
        // Style all elements
        'input': {
            'color': 'blue'
        }, 
        // style valid state
        '.valid': {
            'color': 'green'
        },
        // style invalid state
        '.invalid': {
            'color': 'red'
        },
        // Media queries
        // Note that these apply to the iframe, not the root window.
        '@media screen and (max-width: 400px)': {
            'input': {
                'color': 'orange'
            }
        }
    }
})


order_Btn.addEventListener('click', () => {
    
    const tappayStatus = TPDirect.card.getTappayFieldsStatus()

    // 確認是否可以 getPrime
    if (tappayStatus.canGetPrime === false) {
        error_tip.innerHTML='can not get prime'
        return
    }

    // Get prime
    TPDirect.card.getPrime((result) => {
        if (result.status !== 0) {
            alert('get prime error ' + result.msg)
            return
        }

        let prime = {
            'card': result.card.prime,
            'name': orders_name.value,
            'email': orders_email.value,
            'phone':orders_phone.value
        }
        
        fetch('/api/orders',{
            method:'POST',
            headers:{
                'content-type':'application/json'
            },
            body:JSON.stringify(prime)})
        .then((res) => res.json())
        .then((res) => {
            console.log(res)
            

            if(res.error){
                error_tip.innerHTML = res.message
            }

            if(res.data){
                location.href=`/thankyou?number=${res.data.number}`
            }
        })


        // send prime to your server, to pay with Pay by Prime API .
        // Pay By Prime Docs: https://docs.tappaysdk.com/tutorial/zh/back.html#pay-by-prime-api
    })
})