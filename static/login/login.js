const close = document.querySelector('.close')
const loginBox = document.querySelector('.loginBox')
const select = document.querySelector('.select')
const show = document.querySelector('.show')
const register_show = document.querySelector('.register_show')
const registeredBox = document.querySelector('.registeredBox')
const register_close = document.querySelector('#register_close')
const click_register = document.querySelector('#click_register')
const login_click = document.querySelector('#login_click')
const schedule = document.querySelector('#schedule')
const who = document.querySelector('#who')
let booking_status = false
select.addEventListener('click', () => {
    if(select.textContent == '登出'){
        fetch('/api/user', {
            method:'DELETE',
            headers: {
            "content-type": "application/json",
          }})
        .then(res => res.json())
        .then(res => {
            if(res.ok){
                select.textContent = '登入/註冊'
                window.location.reload()
            }
        })
    }else{
        loginBox.classList.remove('active')
    }
    
})


close.addEventListener('click', () => {
    loginBox.classList.add('active')
})

show.addEventListener('click', () => {
    loginBox.classList.add('active')
})

register_close.addEventListener('click', () =>{
    registeredBox.classList.add('active')
})

register_show.addEventListener('click', () => {
    registeredBox.classList.add('active')
})

click_register.addEventListener('click', () => {
    loginBox.classList.add('active')
    registeredBox.classList.remove('active')
})

login_click.addEventListener('click', () => {
    registeredBox.classList.add('active')
    loginBox.classList.remove('active')
})

async function init_status(){
    const fetch_user = await fetch('/api/user')
    const user_json = await fetch_user.json()
    if(user_json.data == null) return 
    if (user_json.error) {
        console.log(res.error)
    }

    if(user_json.data) {
        select.textContent='登出'
        
        if (booking_status){
            who.textContent = user_json.data.name
        }
    }else{
        console.log(user_json)
    }
    
    
} 


init_status()


    

const login = document.getElementById('login')
const login_tip = document.getElementById('login_tip')
login.addEventListener('click', (e) => {
    e.preventDefault()
    let data = {
        email: document.getElementById('email').value,
        password: document.getElementById('password').value
    }
    fetch('/api/user', {
        method: 'PATCH',
        headers: {
            "content-type": "application/json",
          },
        body:JSON.stringify(data)})
    .then((res) => res.json())
    .then((data) => {
        if(data.error){
            login_tip.textContent= data.message
        }
        if(data.ok){
            select.textContent = '登出'
            login_tip.textContent =  '成功登入'
            setTimeout(() =>{
                window.location.reload()
            },2000) 
        }
    })
    .catch(err => console.log(err))
})

const registerBtn = document.getElementById('registerBtn')
const register_tip = document.getElementById('register_tip')
registerBtn.addEventListener('click', (e) => {
    const RS_name = document.getElementById('register_name')
    const RS_email = document.getElementById('register_email')
    const RS_password = document.getElementById('register_password')
    e.preventDefault()
    let data = {
        name: RS_name.value,
        email:RS_email.value,
        password:RS_password.value
    }
    fetch('/api/user', {
        method:'POST',
        headers: {
            "content-type": "application/json",
        },body:JSON.stringify(data)})
    .then(res => res.json())
    .then(res => {
        if(res.ok){
            register_tip.textContent = '註冊成功'
            RS_name.value= ''
            RS_email.value= ''
            RS_password.value = ''
        }else{
            register_tip.textContent = res.message
        }
    })
})

schedule.addEventListener('click', ()=>{
    if(login_status){
        window.location.href = '/booking'
    }
    else{
        loginBox.classList.remove('active')
    }
})

