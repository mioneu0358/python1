window.addEventListener('DOMContentLoaded',function() {
    let submit = this.document.querySelector('#submit');
    submit.addEventListener('click', function() {
    submitData();
    })
})

async function submitData() {
    let year = document.querySelector('#input-year').value;
    let month = document.querySelector('#input-month').value;
    let day = document.querySelector('#input-day').value;

    let incident = document.querySelector('#input-incident').value;
    let name = document.querySelector('#input-name').value;
    year = year? year: 0;
    month = month? month : 0;
    day = day? day: 0;



    try {
        let response = await fetch('/db/getdata', {
            method  : 'POST',
            headers : {
                'Content-Type': 'application/json'
            },
            body    : JSON.stringify({
                year    :   year,
                month   :   month,
                day     :   day,
                incident:   incident,
                name    :   name        
            })
        });
        let result = await response.json();
        console.log('result: ', result);
    } catch(e) {
        console.error(e);
        alert('에러가 발생했습니다. 관리자에게 문의하세요.');
    }

}