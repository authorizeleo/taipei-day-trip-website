
let order_number = window.location.href.split("=")[1];
const thankyou_name = document.getElementById('thankyou_name')
const thankyou_number = document.getElementById('thankyou_number')
const thankyou = document.querySelector('.thankyou')
fetch(`/api/order/${order_number}`)
.then((res) => res.json())
.then((res) => {
    // console.log(res)
    if(res.login_error) {
        window.location.href = '/'
    }

    if(res.data){
        thankyou_name.textContent = res.data.contact.name
        thankyou_number.textContent = res.data.number
    }
    
    if(res.error){
        thankyou.innerHTML ='錯誤訂購號碼'
        setTimeout(() => window.location.href ='/', 4000)
        
    }

    
})