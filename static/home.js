const footer = document.querySelector('.footer')
const search = document.getElementById('search')
const Search_Btn = document.querySelector('.searchBtnBox')
const list = document.getElementById('sightseeingBox')
let filter = false
let check_index = true
let num = 0 ;
let api = '/api/attractions?page=' + num;
let delay_get_data = debounce(getData)

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

const fetch_data = (api_data) => {
     fetch(api_data)
      .then((res) => {
        return res.json();
      })
      .then((myJson) => {
        for_data(myJson)
        num = myJson[0]['nextPage']
        api = '/api/attractions?page=' + num
      }); 
}

window.onload = () => {
  fetch_data(api)
}


window.addEventListener('scroll', () => {
  const { bottom } = footer.getBoundingClientRect()
  if(window.innerHeight + 1   > bottom){
    if(check_index){
      delay_get_data()
    }
    if(filter){
      delay_connect()
    }
  }   
})


async function connect_filter_data(){
  if(page == null) return
  await search_data(search_api)
}

let delay_connect = debounce(connect_filter_data)
const create_sightseeing = (id, img, title, mrt, cat2) => {
    const a_href = document.createElement('a')
    const sightseeing = document.createElement('DIV')
    const sightseeing_img = document.createElement('DIV')
    const sightseeing_title = document.createElement('H4')
    const sightseeing_main = document.createElement('DIV')
    const sightseeing_mrt = document.createElement('P')
    const sightseeing_cat2 = document.createElement('P')
    sightseeing.className = 'sightseeing'
    sightseeing_img.className = 'sightseeing-img'
    sightseeing_title.className = 'sightseeing-title'
    sightseeing_main.className ='sightseeing-main'
    a_href.href = '/attraction/' + id
    a_href.style.textDecoration = 'none'
    sightseeing_img.style.backgroundImage= `url(${img})`
    sightseeing_title.textContent = title
    sightseeing_mrt.textContent = mrt
    sightseeing_cat2.textContent = cat2
    list.appendChild(a_href)
    a_href.appendChild(sightseeing)
    sightseeing.appendChild(sightseeing_img)
    sightseeing.appendChild(sightseeing_title)
    sightseeing.appendChild(sightseeing_main)
    sightseeing_main.appendChild(sightseeing_mrt)
    sightseeing_main.appendChild(sightseeing_cat2)
}


async function getData() {
    if(num == null) return
    await fetch_data(api)
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
  check_index = false
  filter = true
  page = 0
  search_api = `/api/attractions?page=${page}&keyword=${search.value}`  
  list.innerHTML = "" 
  if(page == null) return
  search_data(search_api) 
})


const search_data = ((api_data) => {
    fetch(api_data)
      .then((res) => {
        return res.json()
      })
      .then((myJson) => {
        for_data(myJson)
        page = myJson[0]['nextPage']
        if(page == null) return
        search_api = `/api/attractions?page=${page}&keyword=${search.value}` 
      })
      .catch(() => list.textContent = '無任何相關景點')
})