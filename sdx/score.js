var argvs = process.argv.slice(2)

var  item = {"enrollId":parseInt(argvs[0]),"lowScore":parseInt(argvs[1]),"lowRank":parseInt(argvs[2])}

function o(e){try{var n=e.lowScore,t=e.enrollId;if(!n||isNaN(t))return e;var a=e.et;if(2==a&&(n=s(n)),!isNaN(n)&&n>900){n-=900;var o=e.lowRank,r=function(e,n){var t=e%157;0==t&&(t=1);t+=26;var a=n%t,o=(n-a)/7/t;return o*(t-26)+a}(t,n),i=o-r;e.lowScore=r,e.lowRank=i,t=e.enrolled,isNaN(t)||(e.enrolled=t-r),t=e.averageScore,isNaN(t)||(e.averageScore=t-r),t=e.averageRank,isNaN(t)||(e.averageRank=t-r),t=e.highScore,isNaN(t)||(e.highScore=t-r),t=e.highRank,isNaN(t)||(e.highRank=t-r),t=e.line,isNaN(t)||(e.line=t-r),t=e.batchScoreDiff,isNaN(t)||(e.batchScoreDiff=t-r)}}catch(c){}return e}

var res = o(item)

console.log(res["enrollId"],res["lowScore"],res["lowRank"])
