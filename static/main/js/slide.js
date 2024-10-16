document.addEventListener("DOMContentLoaded", function () {
  const roadList = document.getElementById("road-list");
  const leftArrow = document.getElementById("left-arrow");
  const rightArrow = document.getElementById("right-arrow");

  let moveX = 0;
  const cardWidth = 260;
  const containerWidth = 900;
  const cardCount = 10;
  let totalX = cardWidth * cardCount;
  let autoSlideInterval;
  let direction = "left"; // 슬라이드 방향 추가

  // 카드 생성
  for (let i = 0; i < cardCount; i++) {
     const imageUrl = `${staticImagePath}slide${i+1}.jpg`;
     console.log(imageUrl); // 이미지 URL을 콘솔에 출력해 확인
    const card = document.createElement("div");
    card.className = "card";
    card.innerHTML = `
      <img src="${imageUrl}" width="100%" height="200px" alt="Image">
      <div class="card-content">
        <div class="card-type">My name</div>
        <div class="card-part">John</div>
      </div>
      <div class="card-content">
        <div class="card-title">thinking</div>
      </div>
    `;
    roadList.appendChild(card);
  }

  function updateSlide(manualDirection) {
    // 수동 방향이 있는 경우 이를 우선시
    if (manualDirection) {
      direction = manualDirection;
    }

    // 한 번에 두 개씩 슬라이드 이동하도록 수정
    const moveAmount = cardWidth * 2;

    if (direction === "left" && totalX >= containerWidth) {
      moveX -= moveAmount;
      totalX -= moveAmount;
    } else if (direction === "right" && moveX < 0) {
      moveX += moveAmount;
      totalX += moveAmount;
    }

    roadList.style.transform = `translateX(${moveX}px)`;

    // 화살표 투명도 업데이트
    leftArrow.style.opacity = totalX >= containerWidth ? 1 : 0.2;
    rightArrow.style.opacity = moveX < 0 ? 1 : 0.2;
  }

  leftArrow.addEventListener("click", function () {
    updateSlide("left");
    resetAutoSlide();
  });

  rightArrow.addEventListener("click", function () {
    updateSlide("right");
    resetAutoSlide();
  });

  // 자동 슬라이드 기능
  function autoSlide() {
    if (direction === "left") {
      if (moveX - cardWidth >= -((cardCount - 1) * cardWidth)) {
        moveX -= cardWidth;
      } else {
        direction = "right"; // 왼쪽 끝에 도달하면 방향 변경
      }
    } else if (direction === "right") {
      if (moveX + cardWidth <= 0) {
        moveX += cardWidth;
      } else {
        direction = "left"; // 오른쪽 끝에 도달하면 방향 변경
      }
    }
    roadList.style.transform = `translateX(${moveX}px)`;
  }

  function startAutoSlide() {
    autoSlideInterval = setInterval(autoSlide, 3000);
  }

  function resetAutoSlide() {
    clearInterval(autoSlideInterval);
    startAutoSlide();
  }

  startAutoSlide();
});