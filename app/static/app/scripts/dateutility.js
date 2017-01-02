function todays_date(){
	return new Date();
}

function str_todays_date(){
	return gettoday()+' '+gettime();
}
function todays_year(){
	return todays_date().getFullYear();
}
function todays_day(){
	return todays_date().getDate();
}
function todays_month(){
	return todays_date().getMonth();
}

function todays_hours(){
	return todays_date().getHours();
	
}
function todays_minutes(){
	return todays_date().getMinutes();
	
}
function todays_seconds(){
	return todays_date().getSeconds();
	
}
function gettoday(){
	return todays_year()+'/'+todays_month()+'/'+todays_day();
}




function gettime(){
	return todays_hours()+':'+todays_minutes()+':'+todays_seconds();
}
function getfulldate(){
	gettoday()+' '+gettime();
}
function hourtomilli(param){
	return param*60*60*1000;
}
function mintomilli(param){
	return param*60*1000;
}
function sectomilli(param){
	return param*1000;
}
function now_addminutes(param){
	return new Date(todays_date().getTime()+mintomilli(param));
}
function addminutes_totime(param,param_t){
	//var fulld=gettoday()+' '+param_t;
	var result=mintomilli(param)+new Date(param_t).getTime();
	return new Date(result);
}

function subtract_fromfinal(param,param_t){
	return new Date( todays_date().getTime()+mintomilli(param))-(new Date(param_t).getTime());
}
function get_str_from_datetime(param_t){
	var d=new Date(param_t);
	var y=d.getFullYear();
	var m=d.getMonth()+1;
	var day=d.getDate();
	var h=d.getHours();
	var min=d.getMinutes();
	var sec=d.getSeconds();
	var new_str=y+'/'+m+'/'+day+' '+h+':'+min+':'+sec;
	return new_str;
	
	
	
}
