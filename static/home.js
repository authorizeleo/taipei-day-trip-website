const footer = document.querySelector('.footer')
const search = document.getElementById('search')
const Search_Btn = document.querySelector('.searchBtnBox')
const list = document.getElementById('sightseeingBox')


let num = 0 ;
let api = '/api/attractions?page=' + num;

fetch(api)
  .then((res) => {
    return res.json();
  })
  .then((myJson) => {
    for (let x = 0; x < myJson.length; x++ ){
        let img = myJson[x]['data'][0]['images'][0] 
        let title = myJson[x]['data'][0]['name']
        let mrt = myJson[x]['data'][0]['mrt'] || '無'
        let cat2 = myJson[x]['data'][0]['category']
        create_sightseeing(img, title, mrt, cat2)
    }
    num = myJson[0]['nextPage']
    api = '/api/attractions?page=' + num
}); 




let mix = debounce(getData)
window.addEventListener('scroll', mix)
const create_sightseeing = (img, title, mrt, cat2) => {

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


    sightseeing_img.style.backgroundImage= `url(${img})`
    sightseeing_title.textContent = title
    sightseeing_mrt.textContent = mrt
    sightseeing_cat2.textContent = cat2

    
    list.appendChild(sightseeing)
    sightseeing.appendChild(sightseeing_img)
    sightseeing.appendChild(sightseeing_title)
    sightseeing.appendChild(sightseeing_main)
    sightseeing_main.appendChild(sightseeing_mrt)
    sightseeing_main.appendChild(sightseeing_cat2)
  }

function getData() {
  const { top } = footer.getBoundingClientRect()
    if(num == null) return
    if ( window.innerHeight + 1  >   top){ 
      fetch(api)
      .then((res) => {
        return res.json();
      })
      .then((myJson) => {
        for (let x = 0; x < myJson.length; x++ ){
            let img = myJson[x]['data'][0]['images'][0] 
            let title = myJson[x]['data'][0]['name']
            let mrt = myJson[x]['data'][0]['mrt'] || '無'
            let cat2 = myJson[x]['data'][0]['category']
            create_sightseeing(img, title, mrt, cat2)
        }
        num = myJson[0]['nextPage']
        api = '/api/attractions?page=' + num
      });
    }
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




Search_Btn.addEventListener('click', () => {
  let page = 0
  let search_api = `/api/attractions?page=${page}&keyword=${search.value}`  
  window.removeEventListener('scroll', mix);
  list.innerHTML = ""
  
  fetch(search_api)
  .then((res) => {
    return res.json()
  })
  .then((myJson) =>{
    for( let x = 0 ; x < myJson.length ; x++) {
      let img = myJson[x]['data'][0]['images'][0] 
      let title = myJson[x]['data'][0]['name']
      let mrt = myJson[x]['data'][0]['mrt'] || '無'
      let cat2 = myJson[x]['data'][0]['category']
      create_sightseeing(img, title, mrt, cat2)
      
    }
     page = myJson[0]['nextPage']
     search_api = '/api/attractions?page='+ page +'&keyword=' + search.value
  })
  .catch(() => {
      list.textContent = '無任何相關景點'
  })

  if (page == null) return
  
  
  const connect = () => {
    if(page == null) return
    if(window.innerHeight  + 1  > footer.getBoundingClientRect().top){
      fetch(search_api)
      .then((res) => {
        return res.json()
      })
      .then((myJson) => {
        for( let x = 0 ; x < myJson.length ; x++) {
          let img = myJson[x]['data'][0]['images'][0] 
          let title = myJson[x]['data'][0]['name']
          let mrt = myJson[x]['data'][0]['mrt'] || '無'
          let cat2 = myJson[x]['data'][0]['category']
          create_sightseeing(img, title, mrt, cat2)
          
        }
         page = myJson[0]['nextPage']
         search_api = '/api/attractions?page='+ page +'&keyword=' + search.value
      })
    }
    
  }
  window.addEventListener('scroll', debounce(connect))
})



