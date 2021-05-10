const close = document.querySelector('.close')
const loginBox = document.querySelector('.loginBox')
const select = document.querySelector('.select')
const show = document.querySelector('.show')
const register_show = document.querySelector('.register_show')
const registeredBox = document.querySelector('.registeredBox')
const register_close = document.querySelector('#register_close')
const click_register = document.querySelector('#click_register')
const login_click = document.querySelector('#login_click')

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
    window.onload = () =>{
         fetch('/api/user',{method:"GET"})
        .then(res => res.json())
        .then(res => {
        if(res.data == null ) return
        if (res.error){
            console.log(res)
        }
        else if(res.data){
            select.textContent='登出'
            console.log(res)
        }else{
            console.log(res)
        }
    })
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
    e.preventDefault()
    let data = {
        name: document.getElementById('register_name').value,
        email:document.getElementById('register_email').value,
        password:document.getElementById('register_password').value
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
        }else{
            register_tip.textContent = res.message
        }
    })
})



