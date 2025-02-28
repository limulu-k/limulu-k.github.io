require('dotenv').config(); // dotenv 불러오기
const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

(async () => {
  const browser = await chromium.launch({ headless: false }); // headless 모드 끄기 (디버깅 가능)
  const context = await browser.newContext();
  const page = await context.newPage();

  console.log("🔹 Notion 로그인 페이지 이동...");
  await page.goto('https://www.notion.so/login');

  // ✅ 이메일 입력
  await page.fill('input[name="email"]', process.env.NOTION_EMAIL);
  await page.click('button[type="submit"]');

  // ✅ 비밀번호 입력 (로그인 화면이 변경될 가능성 고려)
  await page.waitForTimeout(3000); // 페이지 로딩 대기
  await page.fill('input[name="password"]', process.env.NOTION_PASSWORD);
  await page.click('button[type="submit"]');

  // ✅ 로그인 후 페이지 이동
  await page.waitForNavigation();
  console.log("✅ 로그인 성공!");

  // ✅ 특정 Notion 페이지 이동
  await page.goto(process.env.NOTION_PAGE_URL);
  await page.waitForTimeout(5000); // 페이지 로딩 대기

  // ✅ 페이지 내용 저장 (HTML)
  const content = await page.content();
  const outputPath = path.join(__dirname, 'notion_page.html');
  fs.writeFileSync(outputPath, content);
  console.log(`✅ Notion 페이지 저장 완료: ${outputPath}`);

  await browser.close();
})();
