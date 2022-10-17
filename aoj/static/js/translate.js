// const init_lang = 'en';
//
// function TranslateInit() {
//     console.log(123);
//     let code = TranslateGetCode();
//     // Находим флаг с выбранным языком для перевода и добавляем к нему активный класс
//     $('[data-google-lang="' + code + '"]').addClass('language__img_active');
//
//     if (code === init_lang) {
//         // Если язык по умолчанию, совпадает с языком на который переводим
//         // То очищаем куки
//         TranslateClearCookie();
//     }
//
//     // Инициализируем виджет с языком по умолчанию
//     new google.translate.TranslateElement({
//         pageLanguage: code,
//     });
//
// }
//
// function TranslateGetCode() {
//     // Если куки нет, то передаем дефолтный язык
//     return $.cookie('googtrans') ? $.cookie('googtrans') : init_lang;
// }
//
// function TranslateClearCookie() {
//     $.cookie('googtrans', null);
//     // $.cookie("googtrans", null, {
//     //     domain: "." + document.domain,
//     // });
// }
//
// function TranslateSetCookie(code) {
//     // Записываем куки /язык_который_переводим/язык_на_который_переводим
//     $.cookie('googtrans', code);
//     // $.cookie("googtrans", "/en/" + code, {
//     //     domain: "." + document.domain,
//     // });
// }
//
// $(function () {
//     $('#text-img').attr('src', '/static/img/text-' + TranslateGetCode() + '.png');
//
//     //
//     $('a[data-google-lang]').click(function () {
//         TranslateSetCookie($(this).data("google-lang"));
//         window.location.reload();
//     });
// });

function createCookie(name, value, days) {
    var expires;

    if (days) {
        var date = new Date();
        date.setTime(date.getTime() + (days * 24 * 60 * 60 * 1000));
        expires = "; expires=" + date.toGMTString();
    } else {
        expires = "";
    }
    document.cookie = encodeURIComponent(name) + "=" + encodeURIComponent(value) + expires + "; path=/";
}

function readCookie(name) {
    var nameEQ = encodeURIComponent(name) + "=";
    var ca = document.cookie.split(';');
    for (var i = 0; i < ca.length; i++) {
        var c = ca[i];
        while (c.charAt(0) === ' ')
            c = c.substring(1, c.length);
        if (c.indexOf(nameEQ) === 0)
            return decodeURIComponent(c.substring(nameEQ.length, c.length));
    }
    return null;
}

function eraseCookie(name) {
    createCookie(name, "", -1);
}

const googleTranslateConfig = {
    lang: "en",
};

function TranslateInit() {

    let code = TranslateGetCode();
    // Находим флаг с выбранным языком для перевода и добавляем к нему активный класс
    $('[data-google-lang="' + code + '"]').addClass('language__img_active');

    // if (code == googleTranslateConfig.lang) {
    //     // Если язык по умолчанию, совпадает с языком на который переводим
    //     // То очищаем куки
    //     TranslateClearCookie();
    // }

    // Инициализируем виджет с языком по умолчанию
    new google.translate.TranslateElement({
        pageLanguage: googleTranslateConfig.lang,
    });

    // Вешаем событие  клик на флаги

}

function TranslateGetCode() {
    // Если куки нет, то передаем дефолтный язык
    let lang = readCookie('googtrans') ? readCookie('googtrans') : googleTranslateConfig.lang;
    return lang.substr(-2);
}

function TranslateClearCookie() {
    eraseCookie('googtrans');
}

function TranslateSetCookie(code) {
    // Записываем куки /язык_который_переводим/язык_на_который_переводим
    createCookie('googtrans', "/auto/" + code);
}

$(function () {
    $('#text-img').attr('src', '/static/img/text-' + TranslateGetCode() + '.png');

    // $('a[data-google-lang]').click(function () {
    //     TranslateSetCookie($(this).attr("data-google-lang"))
    //     // Перезагружаем страницу
    //     window.location.reload();
    // });
});