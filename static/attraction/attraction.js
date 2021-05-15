let api_sights = '/api/attraction/' + location.href.split('attraction/')[1]
const sights_name = document.getElementById('name')
const sights_mrt = document.getElementById('mrt')
const sights_cat2 = document.getElementById('cat2')
const sights_des = document.getElementById('des')
const sights_address = document.getElementById('address')
const sights_transport = document.getElementById('transport')
const sights_img = document.querySelector('.Carousel')
const left  = document.querySelector('.CarouselLeft')
const right = document.querySelector('.CarouselRight')
const time_am = document.getElementById('time_am')
const time_pm = document.getElementById('time_pm')
const travel_price = document.getElementById('price')
const ul = document.getElementById('CarouselCircle')
let imgsBox ;

fetch(api_sights)
.then(res => res.json())
.then((myJson) => {
    const json = myJson['data'][0]
    const name = json['name']
    const address = json['address']
    const des = json['description']
    imgsBox = json['images']
    const traffic = json['transport'] || '無大眾運輸工具'
    const mrt = json['mrt'] || '無捷運站'
    const cat2 = json['category']
    input_data(name, imgsBox, mrt, cat2, des, address, traffic)
    produce_circle()
    click_circle()
})



function input_data(name, imgs, mrt, cat2, des, address, traffic) {
    input_image(imgs)
    sights_name.textContent = name
    sights_mrt.textContent = mrt
    sights_cat2.textContent = cat2
    sights_des.textContent = des
    sights_address.textContent = address
    sights_transport.textContent = traffic
}

let num = 0
let pos = 0
left.addEventListener('click', () => {
    let calc_length = imgsBox.length-1
    pos += 100
    pos = pos == 100  ? calc_length * -100 : pos
    move_image(pos)
    num--
    num = num < 0 ?  calc_length : num
    change_circle_color(num)
})

right.addEventListener('click', () => {
    let calc_length = imgsBox.length-1
    pos -= 100
    pos = pos == calc_length * -100 -100  ? 0 : pos
    move_image(pos)
    num++
    num = num > calc_length ?  0 : num
    change_circle_color(num)
})

time_am.addEventListener('change', () => {
    travel_price.textContent = '新台幣：2000元'
})

time_pm.addEventListener('change', () => {
    travel_price.textContent = '新台幣：2500元'
})


const produce_circle = (() => {
    for(let x = 0; x < imgsBox.length; x++) {
        let li = document.createElement('li')
        ul.appendChild(li)
    }
})

const click_circle = (() =>{
    let circle_all = document.querySelectorAll('#CarouselCircle >  li' )
    circle_all.forEach((img, i) => {
        img.addEventListener('click', () => {
            num = i
            pos = num * -100
            change_circle_color(num)
        })
    })
})

const change_circle_color = ((n) => {
    let li_all = document.querySelectorAll('#CarouselCircle >  li' )
    img_change(n)
    li_all.forEach((img, i ) => {
        img.style.backgroundColor = n == i ? 'black' :'white'
    })
})

const input_image = ((imgs) => {
    imgs.forEach((img, i ) => {
        const image = document.createElement('img')
        image.src = img
        image.className = 'image-loading'
        const image_li = document.createElement('li')
        image_li.appendChild(image)
        sights_img.appendChild(image_li)
        if( i != 0){
            image_li.classList.add('unseen')
        }
        image.addEventListener('load', () => {
            image.classList.remove('image-loading')
            image.classList.add('sights_img')
        })
    })
})

const img_change = ((n)=>{
    const image_li = document.querySelectorAll('.Carousel > li')
    image_li.forEach((li,i) =>{   
        li.classList.add('unseen')
        li.style.transform = `translateX(${n*-100}%)`
        if( i == n) {
            li.classList.remove('unseen')
        }
    })
})

const move_image = (p) => {
    const move_img = document.querySelectorAll('.Carousel > li ')
    move_img.forEach( li=> {
        li.style.transform = `translateX(${p}%)`
    })
}