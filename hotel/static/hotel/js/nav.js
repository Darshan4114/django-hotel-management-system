const ham = document.getElementById("ham");
const navlistDiv = document.querySelector("#navlist-div");
const navList = document.querySelector("#navlist");
const nav = document.getElementById("navbar");
const vw = Math.max(
  document.documentElement.clientWidth || 0,
  window.innerWidth || 0
);
//  const ham = document.getElementById('ham-div').firstChild;
var width, height;
window.onresize = window.onload = function () {
  width = this.innerWidth;
  height = this.innerHeight;
  if (width > 599) {
    ham.classList.add("hidden");
    ham.classList.remove("ham-on");
    navlist.classList.add("open-nav");
    navlist.classList.remove("hidden");
  } else {
    ham.classList.remove("hidden");
    navlist.classList.remove("open-nav");
    navlist.classList.add("hidden");
  }
};

function togglenav() {
  // const ham = document.getElementById('ham-div').firstChild;
  ham.classList.add("ham-off");

  if (navlist.classList.contains("hidden")) {
    navlist.classList.toggle("hidden");
    // navlistDiv.classList.toggle('open-nav');
    ham.classList.replace("ham-off", "ham-on");
  } else {
    navlist.classList.toggle("hidden");
    ham.classList.replace("ham-on", "ham-off");
    // navlist.classList.toggle('open-nav')
  }
}
