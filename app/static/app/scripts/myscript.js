
$(function () {

    if (Cookies.get('start_time', { path: '/questionpage' }) == undefined) {
        console.log('fresh...........................................................');
    } else {
        console.log('not so fresh...........................................................');
    }

   

    $(':radio, :checkbox').change(function () {
        $("#post").text('Submit');
    })

    
    $('#startbtn').click(function (e) {
        e.preventDefault();
        
            window.location = '/questionpage?module=' + $('#modselect').val();
            //alert($('#modselect').val())
        });

    $('#prev').click(function () {

        window.location = '/questionpage/' +'prev';
    })
     var progress='<span  class="progress">\t  Posting .....</span>'
    $('#post').click(function () {
        //console.log(timepart() + '.............................')
       $('#post').append(progress)
        var x = ""
        $(':radio, :checkbox').each(function (i) {
            if (this.checked) {
                x = x + i + '-';
            }
        })
        //alert($('#qnum').html().trim());
        $.get("/postanswer", { data: x })
            .done(function (data) {
                $('#post')
                    .text('Done !!!')
                    
                    .addClass('btn-success');
                //setcolor(data.data);
                
            });


    });


    $.get("/get_answer", {})

           .done(function (data) {
               console.log('£££££££££££££££££££££££££££££££££££££££££££££££££££££££££ myans' + data.ans)
               //console.log('£££££££££££££££££££££££££££££££££££££££££££££££££££££££££ myque' + data.ques)
               setcolor(data.ques,data.ans);

           });

    var queslist = $('#qlist').html();
   // var myans = $('#anslist').html();
    var l = ['z', 'c', 'v']

    //console.log('---' + JSON.parse(myans))
    
    //console.log('$$$$$$$$$$$$$$$$$$$$$$ link' + links[8])
    
    var setcolor = function (ques,ans) {
        
        var links = $('.pagination li a');
        $.each(links, function (i, v) {
            console.log(ques[i]+' ----------- '+i)
            
            if (ans.indexOf(ques[$(v).html()-1]) > 0) {
                console.log('^^^^^^^^^^^^^^^^^^^^^^ match')
                $(v).css({'color':'green'})
            }
        })
       
        
    }

    //setcolor();


    setInterval(function () {
        var newdate=new Date();
        var d = newdate.getDate() + "-" + newdate.getMonth() + "-" + newdate.getFullYear() + "  " + newdate.getHours()+":"+newdate.getMinutes()+":"+newdate.getSeconds();
        $('.countdowspot').html(d);
        //alert('don');
        
    }, 1000);



    var mygetdate = function () {
       
        var du = $('#duration').html().trim();
        console.log('duration.....................................'+du)
        var mydate = now_addminutes(du);
        return mydate;
    }

    var datepart = function () {
        var parts = mygetdate().split(' ')
        return parts[0]
    }
    var timepart = function () {
        var parts = mygetdate().split(' ');
        
        return parts[1]
    }
    
    $(window).on('unload', function () {
        var cval = $('#timespot').html().trim();
        //if (cval == "00:00:00"){
        console.log('setting timeval.........................................................')
        Cookies.set('timeval', cval, { path: '/questionpage' });
       
    })

    //window.onbeforeunload = function () {
    //    var cval= $('#timespot').html().trim();
    //    //if (cval == "00:00:00"){
    //    console.log('setting timeval.........................................................')
    //    Cookies.set('timeval', cval,{ path: '/questionpage' });
    //    //}
    //}
    var ct = function (cdp) {

        console.log('cdp ...............................................' + get_str_from_datetime(cdp));
        $('#timespot').countdown(get_str_from_datetime(cdp))
       .on('update.countdown', function (event) {
           $(this).html(event.strftime('%H:%M:%S'));
           //$('#timepart').html(timepart())


       })
       .on('finish.countdown', function () {
           Cookies.remove('start_time', { path: '/questionpage' })
           Cookies.remove('timeval', { path: '/questionpage' })
           window.location = '/reset';

           //window.location = '/boardpage';

       });
    }
    var initval = function () {
        console.log('mygetdate().....................................' + mygetdate());
        
         countdown_param = mygetdate();
        if ((Cookies.get('start_time') == undefined)) {
            Cookies.set('start_time', mygetdate(), { path: '/questionpage' });
            
        }
        console.log('set start_time to.............................' + Cookies.get('start_time'));
        if ((Cookies.get('timeval') != undefined) ){
            
            countdown_param = Cookies.set('timeval');
            var t1 = new Date( Cookies.get('start_time'))
            if (new Date(countdown_param).getHours() > 0) {
                t1.setHours(-1 * (new Date(countdown_param).getHours()));
            }
            if (new Date(countdown_param).getMinutes() > 0) {
                t1.setMunites(-1 * (new Date(countdown_param).getMunites()));
            }
            if (new Date(countdown_param).getSeconds() > 0) {
                t1.setSeconds(-1 * (new Date(countdown_param).getSeconds()));
            }
            console.log('setting countdown_param to.............................' + t1)
            countdown_param = t1;
        }
        console.log('Passing ' + countdown_param + ' to countdown_param.......................................');
        ct(countdown_param);

    }
    initval();
  
    $('#logoff').click(function () {
        console.log('off *******************************************');
        ct(gettoday()+ ' 00:00:00');

    })
    //$('#timespot').countdown('stop');
    
    //setTimeout(function () { $('#timespot').countdown('start'); }, 5000);
    //console.log('prev-ans ' + $('#prev_ans').html());
    if ($('#prev_ans').html() != "") {
        var ans = $('#prev_ans').html();
        var anslist = ans.split('-');
        var newlist = []
        $.each(anslist, function (i, e) {
           
            newlist.push(e)
        })
        
        if ($(':radio').length>0){
            $(':radio')[parseInt(newlist[0])].checked = true;
        }
        //console.log('new list..................................' + newlist);
        if ($(':checkbox').length > 0) {
            $.each(newlist, function (i, e) {
                //console.log('ppppppppppppppp.............' + parseInt(newlist[e]))
                $(':checkbox')[parseInt(e)].checked = true;
            })
        }
    }


    

    })
