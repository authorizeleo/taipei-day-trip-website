let api = '/api/attraction/' + location.href.split('attraction/')[1]
const sight_name = document.getElementById('name')
const sight_mrt = document.getElementById('mrt')
const sight_cat2 = document.getElementById('cat2')
const sight_des = document.getElementById('des')
const sight_address = document.getElementById('address')
const transport = document.getElementById('transport')
const sightseeing_img = document.getElementById('imgBox')
const left  = document.getElementById('left')
const right = document.getElementById('right')
const time_am = document.getElementById('time_am')
const time_pm = document.getElementById('time_pm')
const travel_price = document.getElementById('price')
const ul = document.getElementById('ul')
let imgsBox ;
fetch(api)
    .then(res => res.json())
    .then((myJson) => {
        const json = myJson['data'][0]
        const name = json['name']
        const address = json['address']
        const des = json['description']
        imgsBox = json['images']
        const traffic = json['transport']
        const mrt = json['mrt']
        const cat2 = json['category']
        input_data(name, imgsBox, mrt, cat2, des, address, traffic)
        circle()
        click_imgs()
        const circle_all = document.querySelectorAll('#imgBox > ul > li' )
    })


const input_data = (name, imgs, mrt, cat2, des, address, traffic) => {
    sight_name.textContent = name
    sight_mrt.textContent = mrt
    sight_cat2.textContent = cat2
    sight_des.textContent = des
    sight_address.textContent = address
    transport.textContent = traffic
    sightseeing_img.style.backgroundImage = `url(${imgs[0]})`
    sightseeing_img.style.opacity =1
}

let num = 0
left.addEventListener('click', () => {
    let li_all = document.querySelectorAll('#imgBox > ul > li' )
    num--
    num = num < 0 ?  imgsBox.length-1 : num
    sightseeing_img.style.backgroundImage = `url(${imgsBox[num]})`
    sightseeing_img.style.opacity = 1
    sightseeing_img.style.transition = 0.5 + 's'
    li_all.forEach((img, i ) => {
        console.log(num == i)
        if(num == i ) {
            console.log(img)
            img.style.backgroundColor = 'black'
        }else{
            img.style.backgroundColor = 'white'
        }
    })
    
})

right.addEventListener('click', () => {
    let li_all = document.querySelectorAll('#imgBox > ul > li' )
    num++
    num = num > imgsBox.length-1 ?  0 : num
    sightseeing_img.style.backgroundImage = `url(${imgsBox[num]})`
    sightseeing_img.style.opacity = 1
    sightseeing_img.style.transition = 0.5 + 's'
    li_all.forEach((img, i ) => {
        if(num == i ) {
            img.style.backgroundColor = 'black'
        }else{
            img.style.backgroundColor = 'white'
        }
    })
})

time_am.addEventListener('change', () => {
    travel_price.textContent = '新台幣：2000元'
})

time_pm.addEventListener('change', () => {
    travel_price.textContent = '新台幣：2500元'
})


const circle = ( () => {
    for(let x = 0; x < imgsBox.length; x++) {
        let li = document.createElement('li')
        ul.appendChild(li)
    }
})

const click_imgs = (() =>{
    let circle_all = document.querySelectorAll('#imgBox > ul > li' )
    circle_all.forEach((img, i) => {
        img.addEventListener('click', () => {
            num = i
            circle_all.forEach((ig, index) => {
                if(num == index ) {
                    ig.style.backgroundColor = 'black'
                }else{
                    ig.style.backgroundColor = 'white'
                }
            })
            
            sightseeing_img.style.backgroundImage = `url(${imgsBox[num]})`
            sightseeing_img.style.opacity = 1
            sightseeing_img.style.transition = 0.5 + 's'
        })
    })
})
