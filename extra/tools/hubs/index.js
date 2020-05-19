// -*- mode: js; js-indent-level:2;  -*-
// SPDX-License-Indentifier: MPL-2.0
// Copyright: 2020-present Philippe Coval <https://purl.org/rzr>


// TODO: update once with creds
var url = localStorage['webthings.sense-hat-imu.url'];
// url = 'https://sensehat.mozilla-iot.org/things/sense-hat-imu/properties';

var bearer = localStorage['webthings.sense-hat-imu.bearer'];
// bearer = 'TODO'; // ask rzr

var a = document.querySelectorAll("[gltf-model-plus]");
var o = a[a.length -1];
console.log(o);

var that = { data: { bearer: bearer } };

var headers = {
  Accept: 'application/json'
};
if (that.data.bearer) {
  headers['Authorization'] = `Bearer ${that.data.bearer}`;
}

fetch(url, { headers: headers } ).then((response) => { return response.json();})
  .then((data) => {
    if (!true) console.log(data);
    localStorage['webthings.sense-hat-imu.url'] = url;
    localStorage['webthings.sense-hat-imu.bearer'] = bearer;
  });

var interval = setInterval(function(){
  fetch(url, { headers: headers } ).then((response) => { return response.json();})
    .then((data) => {
      if (true) console.log(data);
      o.object3D.rotation.y = - THREE.Math.degToRad(data.yaw);
    });
}, 1000);

// clearInterval(interval);
