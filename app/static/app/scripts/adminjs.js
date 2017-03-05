$(function () {
    $('.modulebox').on('mouseover', function () {
        $(this).addClass('borderstyle')
    })
    $('.modulebox').on('mouseout', function () {
        $(this).removeClass('borderstyle')
    });


    $(':checkbox').each(function (i) {

        $(this).on('change', function () {
            var x = this.name.replace('_with_', '_')
            if ($(this).is(':checked') == false) {

                $('.field-box.field-' + x).addClass('hidden')
                console.log('..........hide...........')
            } else {
                $('.field-box.field-' + x).removeClass('hidden')
                console.log('..........shown...........')
            }
        })
    })



    $(':checkbox').each(function (i) {

       
            var x = this.name.replace('_with_', '_')
            

                $('.field-box.field-' + x).addClass('hidden')
               
            
        
    })

})