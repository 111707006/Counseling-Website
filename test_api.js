// 測試前端API代理
const fetch = (...args) => import('node-fetch').then(({default: fetch}) => fetch(...args));

async function testAPI() {
  try {
    console.log('Testing frontend proxy...');
    const response = await fetch('http://localhost:3002/api/articles/articles/');
    console.log('Response status:', response.status);
    
    if (response.ok) {
      const data = await response.json();
      console.log('Success! Articles count:', data.length);
      console.log('First article:', data[0]?.title);
    } else {
      console.log('API call failed:', response.statusText);
    }
  } catch (error) {
    console.error('Error:', error.message);
  }
}

testAPI();