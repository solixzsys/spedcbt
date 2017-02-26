$(function () {
    $('.modulebox').on('mouseover', function () {
        $(this).addClass('borderstyle')
    })
    $('.modulebox').on('mouseout', function () {
        $(this).removeClass('borderstyle')
    })
})