window.addEventListener('DOMContentLoaded',function() {
    let submit = this.document.querySelector('#submit');
    submit.addEventListener('click', function() {
    submitData();
    })
})

async function submitData() {
    let year = document.querySelector('#input-year').value;
    let king = document.querySelector('#input-incident').value;
    let content = document.querySelector('#input-name').value;
    year = year? year: 0;
    console.log(year, king, content);


    try {
        let response = await fetch('/db/getdata/category', {
            method  : 'POST',
            headers : {
                'Content-Type': 'application/json'
            },
            body    : JSON.stringify({
                'year'    :   year,
                'king'    :   king,
                'content' :   content
            })
        });
        let result = await response.json();

        console.log('result: ', result);


    } catch(e) {
        console.error(e);
        alert('에러가 발생했습니다. 관리자에게 문의하세요.');
    }

}