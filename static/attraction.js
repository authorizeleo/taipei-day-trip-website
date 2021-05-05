let api = '/api/attraction/' + location.href.split('attraction/')[1]
const sight_name = document.getElementById('name')
const sight_mrt = document.getElementById('mrt')
const sight_cat2 = document.getElementById('cat2')
const sight_des = document.getElementById('des')
const sight_address = document.getElementById('address')
const transport = document.getElementById('transport')
const sightseeing_img = document.querySelector('.Carousel')
const left  = document.querySelector('.CarouselLeft')
const right = document.querySelector('.CarouselRight')
const time_am = document.getElementById('time_am')
const time_pm = document.getElementById('time_pm')
const travel_price = document.getElementById('price')
const ul = document.getElementById('CarouselCircle')
let imgsBox ;
fetch(api)
    .then(res => res.json())
    .then((myJson) => {
        const json = myJson['data'][0]
        const name = json['name']
        const address = json['address']
        const des = json['description']
        imgsBox = json['images']
        const traffic = json['transport'] || '無'
        const mrt = json['mrt'] || '無'
        const cat2 = json['category']
        input_data(name, imgsBox, mrt, cat2, des, address, traffic)
        circle()
        click_circle_imgs()
    })


function input_data(name, imgs, mrt, cat2, des, address, traffic) {
    input_image(imgs)
    sight_name.textContent = name
    sight_mrt.textContent = mrt
    sight_cat2.textContent = cat2
    sight_des.textContent = des
    sight_address.textContent = address
    transport.textContent = traffic
}

let num = 0
left.addEventListener('click', () => {
    num--
    num = num < 0 ?  imgsBox.length-1 : num
    change_bottom_circle(num)
})

right.addEventListener('click', () => {
    num++
    num = num > imgsBox.length-1 ?  0 : num
    change_bottom_circle(num)
})

time_am.addEventListener('change', () => {
    travel_price.textContent = '新台幣：2000元'
})

time_pm.addEventListener('change', () => {
    travel_price.textContent = '新台幣：2500元'
})


const circle = (() => {
    for(let x = 0; x < imgsBox.length; x++) {
        let li = document.createElement('li')
        ul.appendChild(li)
    }
})

const click_circle_imgs = (() =>{
    let circle_all = document.querySelectorAll('#CarouselCircle >  li' )
    circle_all.forEach((img, i) => {
        img.addEventListener('click', () => {
            num = i
            circle_all.forEach((ig, index) => {
                ig.style.backgroundColor = num == index ? 'black' :'white'
            })
            img_change(num)
        })
    })
})

const change_bottom_circle = ((n) => {
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
        const image_li = document.createElement('li')
        if( i != 0){
            image_li.classList.add('space')
        }
        image_li.appendChild(image)
        sightseeing_img.appendChild(image_li)
    })
})

const img_change = ((n)=>{
    const image_li = document.querySelectorAll('.Carousel > li')
    image_li.forEach((li, i) =>{   
        li.classList.add('space')
        if (n == i){
            li.classList.remove('space')
        }
    })
})