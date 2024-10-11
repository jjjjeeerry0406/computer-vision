import * as THREE from 'three';

var render
var scene
var camera

function animateFrame()
{
    //Get the object from scene
    var mesh = scene.getObjectByName('min')
     var mesh1 = scene.getObjectByName('hour')
    if (mesh)
    {        
        var a = new THREE.Vector3( 0, 0, 2 );     
        a.normalize();        
        var ra = new THREE.Matrix4().makeRotationAxis( a , -2.5 / 180 *Math.PI );
        mesh.applyMatrix4(ra);
        mesh.position.set(100, 50, 2)//put the mesh in other coordinate        
    }
    if (mesh1)
    {        
    var a1 = new THREE.Vector3( 0, 0, 1 );     
    a1.normalize();                    
    var ra1 = new THREE.Matrix4().makeRotationAxis( a1 , -2.5/ 180 *Math.PI/12 );
    mesh1.applyMatrix4(ra1);
    mesh1.position.set(100, 50, 1)           
    }
    render.render(scene,camera);
    requestAnimationFrame(animateFrame)
}

function main()
{
    //Scene (as globle var)
    scene = new THREE.Scene();

    //camera (as globle var)
    camera = new THREE.OrthographicCamera( 640 / - 2, 640 / 2, 480 / 2, 480 / - 2, -1000, 1000 );
    camera.position.set(0,0,0);

    //clock's coordinate    
    var clockdot = [];
    clockdot.push( new THREE.Vector3(-50,50, 1 ) );  //0
    clockdot.push( new THREE.Vector3(-25,125, 1 ) ); //1
    clockdot.push( new THREE.Vector3(25,175, 1 )); //2
    clockdot.push( new THREE.Vector3(100,200, 1 ) ); //3
    clockdot.push( new THREE.Vector3(175,175, 1 ) );  //4
    clockdot.push( new THREE.Vector3(225,125, 1 ) ); //5
    clockdot.push( new THREE.Vector3(250,50, 1 )); //6
    clockdot.push( new THREE.Vector3(225,-25, 1 ) ); //7
    clockdot.push( new THREE.Vector3(175,-75, 1 )); //8
    clockdot.push( new THREE.Vector3(100,-100, 1 )); //9
    clockdot.push( new THREE.Vector3(25,-75, 1 )); //10
    clockdot.push( new THREE.Vector3(-25,-25, 1 )); //11

    //min hand's coordinate
    var mindot = [];
    mindot.push( new THREE.Vector3(0,0, 2 ) );  //0
    mindot.push( new THREE.Vector3(0,150, 2 ) ); //1
    mindot.push( new THREE.Vector3(-25,25, 2 )); //2
    mindot.push( new THREE.Vector3(25,25, 2 ) ); //3

    //hour hand's coordinate
    var hourdot = [];
    hourdot.push( new THREE.Vector3(0,0,3 ) );  //0
    hourdot.push( new THREE.Vector3(0,100,3 ) ); //1
    hourdot.push( new THREE.Vector3(-25,25, 3)); //2
    hourdot.push( new THREE.Vector3(25,25,3 ) ); //3

    //
    var clock = [
        0, 2, 1,
        0, 3, 2, 
        0, 4, 3,
        0, 5, 4,
        0, 6, 5,
        0, 7, 6,
        0, 8, 7,
        0, 9, 8,
        0, 10, 9,
        0, 11, 10,                 
    ];
    var min = [
        0, 1 ,2,
        0, 3, 1,
    ]
    var hour = [
        0, 1 ,2,
        0, 3, 1,
    ]
    var geometry1 = new THREE.BufferGeometry().setFromPoints(clockdot);
    geometry1.setIndex( clock );

    var geometry2 = new THREE.BufferGeometry().setFromPoints(mindot);
    geometry2.setIndex( min );

    var geometry3 = new THREE.BufferGeometry().setFromPoints(hourdot);
    geometry3.setIndex( hour );

    //material 
    var material1 = new THREE.MeshBasicMaterial( { color: 0xFFFFFF , wireframe: false} );
    var material2 = new THREE.MeshBasicMaterial( { color: 0x000000 , wireframe: false} );
    var material3 = new THREE.MeshBasicMaterial( { color: 0xFF0000 , wireframe: false} );

    //Mesh (still local var, we will retrive it by getObjectByName)    

    var mesh1 = new THREE.Mesh(geometry1, material1);
    mesh1.name = 'clock'

    var mesh2 = new THREE.Mesh(geometry2, material2);
    mesh2.name = 'min'

    var mesh3 = new THREE.Mesh(geometry3, material3);
    mesh3.name = 'hour'
    
    var gridHelper = new THREE.GridHelper(500,10);
    gridHelper.geometry.rotateX( - Math.PI / 2 );

 
    scene.add(camera);
    scene.add(mesh1);
    scene.add(mesh2);
    scene.add(mesh3);
    scene.add(gridHelper);

    //Render (as globle var)
    render = new THREE.WebGLRenderer();
    render.setClearColor(0x000000,1);
    render.setSize(640,480);
    document.body.appendChild(render.domElement);

    animateFrame();
}
main();