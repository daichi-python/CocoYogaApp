const target = document.getElementById("target");
target.setAttribute("poseAttr", "description");

const poses = document.querySelectorAll(".poses");

function switchPose(step){
    if (target.getAttribute("poseAttr") === "description"){
        const description = document.getElementById("description");
        description.classList.add("invisible");
        poses.item(0).classList.toggle("invisible");
        target.setAttribute("poseAttr", "0");
    } else {
        let index = parseInt(target.getAttribute("poseAttr"));
        poses.item(index).classList.toggle("invisible");

        index += step;
        if (index < 0) index = poses.length -1;
        else if (index >= poses.length) index = 0;

        const nextPose = poses.item(index);
        nextPose.classList.toggle("invisible");

        target.setAttribute("poseAttr", index.toString());
    }
}

const left = document.getElementById("left");
const right = document.getElementById("right");

left.addEventListener("click", () => {
    switchPose(-1);
})

right.addEventListener("click", () => {
    switchPose(1);
})