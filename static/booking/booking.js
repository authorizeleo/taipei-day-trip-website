const del_travel = document.getElementById('trashBox')
const booking_box = document.querySelector('.booking-box')
const booking_title = document.querySelector('.booking-title')
const booking_date = document.querySelector('.booking-date')
const booking_time  = document.querySelector('.booking-time')
const booking_price = document.querySelector('.booking-price')
const booking_address = document.querySelector('.booking-address')
const booking_img = document.querySelector('.booking-img')
const order_price = document.querySelector('#order-price')


booking_status = true
init_status().then(()=> {
    if(login_status === false){
        // window.location.href = '/'
    }else{
        fetch('/api/booking')
        .then((res)=> res.json())
        .then((res) => {
            if(res.error) {
                booking_box.innerHTML ='目前沒有任何待預訂的行程'
                return
            }
            booking_title.textContent = res.attraction.name
            booking_date.textContent = res.date
            res.time = res.time == 'morning' ? '早上 9 點到下午 4 點': '下午 4 點到晚上 11 點'
            booking_time.textContent = res.time
            booking_price.textContent = `新台幣${res.price}元`
            order_price.textContent = `新台幣${res.price}元`
            booking_address.textContent = res.attraction.address
            booking_img.style.backgroundImage = `url(${res.attraction.image})`
        })
    }
})



del_travel.addEventListener('click', () => {
    fetch('/api/booking',
        {
        method: 'DELETE',
        headers: {
            "content-type": "application/json",
        }
        })
        .then((res) => res.json())
        .then((res) => {
            console.log(res)
            if(res.ok){
                booking_box.innerHTML ='目前沒有任何待預訂的行程'
            }
        })
    
})

