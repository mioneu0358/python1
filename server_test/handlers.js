exports.home = (req, res) => {
    res.cookie('monster', 'nom nom');
    res.cookie('signed_monster', 'nom nom', {signed : true});
    res.render('home')};
exports.sectionTest = (req, res) => res.render('section-test');
exports.notFound = (req, res) => res.render('404');
exports.serverError = (err, req, res, next) => {
    console.log(err);
    res.render('500');
}

const VALID_EMAIL_REGEX = new RegExp(
    '^[a-zA-Z0-9.!#$%&\'*+\/=?^_`{|}~-]+@' +
    '[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?' +
    '(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)+$'
    );
// 유저 인터페이스
class NewsletterSignup {
    constructor({name,email}) {
        this.name = name;
        this.email = email;
    }

    async save() {
        // 원래라면, 여기서 데이터를 DB에 저장하는 동작을 정의해야 한다.
        // 이 메서드는 async이므로 promise 객체를 반환하며, 
        // 지금은 예외(에러)없이 함수 호출이 끝날 것이다.
    }
}



exports.newsletterSignup = (req, res) => {
    // CSRF에 대해서는 나중에 알아본다. 지금은 더미 값만 넣어놓자.
    res.render('newsletter-signup', { csrf: 'CSRF token goes here' });
};
exports.newsletterSignupProcess = (req, res) => {
    const name = req.body.name || '';
    const email = req.body.email || '';

    // 입력 유효성 검사
    if (!VALID_EMAIL_REGEX.test(email)) {
        req.session.flash = {
            type: 'danger',
            intro: 'Validation error!',
            message: 'The email address you entered was not valid'
        }
        return res.redirect(303, '/newsletter-signup');
    }

    // NewsletterSignup은 생성할 수 있는 객체의 예제다.
    // 프로그램마다 상황이 다르므로 프로젝트에 밀접한 인터페이스는 직접 작성해줘야 한다.
    // 이 예제는 일반적인 익스프레스 예제가 프로젝트에 어떻게 나타날지 가정할 뿐이다.
    new NewsletterSignup({name, email})
    .save()
    .then(() => {
        req.session.flash = {
            type: 'success',
            intro : 'Thank you!',
            message: 'You have now been signed up for the newsletter.'
        };
        return res.redirect(303,'/newsletter-archive');
    })
    .catch(err => {
        req.session.flash = {
            type: 'danger',
            intro: 'Database error!',
            message: 'There was a database error; please try again later.'
        };
        return res.redirect(303,'/newsletter-archive');
    }); 
};

exports.newsletterArchive = (req,res) => res.render('newsletter-archive');
exports.newsletterSignupThankYou = (req, res) => res.render('newsletter-signup-thank-you');

exports.newsletter = (req, res) => {
    // CSRF에 대해서는 나중에 알아본다. 지금은 더미 값만 넣어놓자.
    res.render('newsletter', { csrf: 'CSRF token goes here' });
};
exports.api = {
    newsletterSignup: (req, res) => {
        // console.log('CSRF token (from hidden form field): ' + req.body._csrf);
        // console.log('Name (from visible form field): ' + req.body.name);
        // console.log('Email (from visible form filed): ' + req.body.email);

        const name = req.body.name || '';
        const email = req.body.email || '';
        const ret = {result: ''};  // 통신 응답 결과

         // 입력 유효성 검사
        if (!VALID_EMAIL_REGEX.test(email)) {
            ret.flash = {
                type: 'danger',
                intro: 'Validation error!',
                message: 'The email address you entered was not valid'
            }
            ret.result = 'error';
            // HTTP CODE 400은 Bad Request. 요청을 처리할 수 없음.
            return res.status(400).send(ret);
        }
        
        new NewsletterSignup({name, email})
        .save()
        .then(() => {
            ret.flash = {
                type: 'success',
                intro: 'Thank you!',
                message: 'You have now been signed up for the newsletter.'
            };
            ret.result = 'success';
            res.send(ret);
        })
        .catch(err => {
            ret.flash = {
                type: 'danger',
                intro: 'Database error!',
                message: 'There was a database error; please try again later.'
            };
            ret.result = 'error';
            res.status(500).send(ret);
        });
    }
};

exports.vacationPhotoContest = (req, res) => {
    const now = new Date()
    res.render('contest/vacation-photo', { 
        year: now.getFullYear(), 
        month: now.getMonth() 
    });
};
exports.vacationPhotoContestProcessError = (req, res) => {
    res.render('contest/vacation-photo-error');
};
exports.vacationPhotoContestProcessThankYou = (req, res) => {
    res.render('contest/vacation-photo-thank-you');
};
exports.vacationPhotoContestProcess = (err, req, res, fields, files) => {
    if (err) return res.redirect(303, '/contest/vacation-photo-error');
    console.log('field data: ', fields);
    console.log('files: ', files);
    res.redirect(303, '/contest/vacation-photo-thank-you');
};


exports.vacationPhotoContestAjax = (req, res) => {
    const now = new Date();
    res.render('contest/vacation-photo-ajax', { 
        year: now.getFullYear(), 
        month: now.getMonth() 
    });
}
exports.api.vacationPhotoContest = (err, req, res, fields, files) => {
    if (err) return res.send({ result: 'error', error: err.message });
    console.log('field data: ', fields);
    console.log('files: ', files);
    res.send({result: 'success'});
}

