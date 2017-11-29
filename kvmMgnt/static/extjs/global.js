//post data to server
function serverConnectPost(data){
    var value = data;
    var rcode = " ";
    $.ajax({
        url:"http://192.168.32.23:8085/api/v0.1/crontrol",
        contentType:"application/json;charset=utf-8",
        type:"POST",
        dataType:"json",
        async:false,
        data:JSON.stringify(value),
        success:function (rdata){
            rcode = rdata
        }
    });
    return rcode
}

//domain crontrol function

function pageSwitch(page,UUID=0){
    if ( page == 'instanceMgnt' ) {
        document.getElementById('list').src = '/instanceMangnt'
    } else if ( page == 'diskMgnt') {
        document.getElementById('list').src = '/diskMangnt'
    } else if (page == 'clusterMgnt') {
        document.getElementById('list').src = '/clusterMangnt'
    } else if (page == 'createDomain') {
        document.getElementById('list').src = '/createDomain'
    } else if (page == 'console') {
        document.getElementById('list').src = '/consoleTop'
    } else if (page == 'userInterface') {
        document.getElementById('list').src = '/userInterface'
    } else if (page == 'domainConfig') {
        document.getElementById('list').src = '/domainConfig'
    } else if (page == 'addNode') {
        window.parent.document.getElementById('list').src = '/clusterNodeAdd'
    } else if (page == 'clusterNodeInformation') {
        window.parent.document.getElementById('list').src = '/clusterNodeResourceInformation/' + UUID
    }
}

function infoFlush(page){
   window.parent.zhezhao1();
    if ( page == 'diskRefer') {
        data = {'type' : 'infoRefer','data' : {'type':'diskAllRefer'}}
        retrunCode = serverConnectPost(data)
        window.parent.zhezhao1();
    }
                window.location.reload();
}
function createDomainInfo(){
    var data = {"type":"getInstanceCreateInfo"}
    recode = serverConnectPost(data)
}

