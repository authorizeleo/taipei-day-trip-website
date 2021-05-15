const search = document.getElementById('search')
const searchBox =document.querySelector('.searchBox')
const Search_Btn = document.querySelector('.searchBtnBox')
const sightseeing_list = document.getElementById('sightseeingBox')
let filter_show = false
let init_show = true
let init_page = 0 ;
let api_home = '/api/attractions?page=' + init_page;
let delay_get_data = debounce(getData)
let data_init = []
const for_data = (data) =>{
  data.forEach(d => {
    let myData = d.data[0]
    let id = myData['id']
    let img = myData['images'][0] 
    let title = myData['name']
    let mrt = myData['mrt'] || '無'
    let cat2 = myData['category']
    create_sightseeing(id, img, title, mrt, cat2)
  });
}

async function fetch_data(api_data){
    const show_data = await fetch(api_data)  
    data_init = await show_data.json() 
    for_data(data_init)
    init_page = data_init[0]['nextPage']
    api_home = '/api/attractions?page=' + init_page 
}

fetch_data(api_home)



window.addEventListener('scroll', () => {
  const { bottom } = document.querySelector('.footer').getBoundingClientRect()
  if(window.innerHeight + 800  > bottom){
    if(init_show){
      delay_get_data()
    }
    if(filter_show){
      delay_filter_data()
    }
  }   
})


function connect_filter_data(){
  if(page == null) return
  search_data(search_api)
}

function getData() {
  if(init_page == null) return
  fetch_data(api_home)
} 

let delay_filter_data = debounce(connect_filter_data)
async function create_sightseeing(id, img, title, mrt, cat2){
    const a_href = document.createElement('a')
    const sightseeing = document.createElement('DIV')
    const sightseeing_img = document.createElement('DIV')
    const sightseeing_title = document.createElement('H4')
    const sightseeing_main = document.createElement('DIV')
    const sightseeing_mrt = document.createElement('P')
    const sightseeing_cat2 = document.createElement('P')
    const imgs = new Image()
    imgs.src = img
    imgs.className = 'circle-loading'
    sightseeing.className = 'sightseeing'
    sightseeing_img.className = 'sightseeing-img'
    sightseeing_title.className = 'sightseeing-title'
    sightseeing_main.className ='sightseeing-content'
    a_href.href = '/attraction/' + id
    sightseeing_title.textContent = title
    sightseeing_mrt.textContent = mrt
    sightseeing_cat2.textContent = cat2
    sightseeing_list.appendChild(a_href)
    a_href.appendChild(sightseeing)
    sightseeing.appendChild(sightseeing_img)
    sightseeing_img.appendChild(imgs)
    sightseeing.appendChild(sightseeing_title)
    sightseeing.appendChild(sightseeing_main)
    sightseeing_main.appendChild(sightseeing_mrt)
    sightseeing_main.appendChild(sightseeing_cat2)

    imgs.addEventListener('load', () => {
      imgs.classList.remove('circle-loading')
      imgs.className = 'image'
    })
}


  

function debounce(func, delay=800) {
    let timer = null;
    return () => {
      let context = this;
      let args = arguments;
      clearTimeout(timer);
      timer = setTimeout(() => {
        func.apply(context, args);
      }, delay)
    }
}

let page = null
let search_api = null
Search_Btn.addEventListener('click', () => {
  search_method()
})


async function search_data(api_data){
  try{
    const search_fetch = await fetch(api_data)  
    const search_result = await search_fetch.json()
    for_data(search_result)
    page = search_result[0]['nextPage']
    if (page == null) return 
    search_api = `/api/attractions?page=${page}&keyword=${search.value}` 
  }catch{
    sightseeing_list.textContent = '無任何相關景點'
  }
}

searchBox.addEventListener('submit', (e)=>{
  e.preventDefault()
  search_method()
})

function search_method(){
  init_show = false
  filter_show = true
  page = 0
  search_api = `/api/attractions?page=${page}&keyword=${search.value}`  
  sightseeing_list.innerHTML = "" 
  if(page == null) return
  search_data(search_api) 
}