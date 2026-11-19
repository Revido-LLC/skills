import { test, expect } from '@playwright/test';

test('staff can log in and place an order', async ({ page }) => {
  await page.goto('/login');
  await page.fill('[name=email]', process.env.TEST_USER_EMAIL!);
  await page.fill('[name=password]', process.env.TEST_USER_PASSWORD!);
  await page.click('button:has-text("Sign in")');
  await expect(page.locator('h1')).toHaveText('Orders');

  await page.click('button:has-text("New order")');
  await page.fill('[name=amount]', '1000');
  await page.click('button:has-text("Place order")');
  await expect(page.locator('.order-row').first()).toContainText('pending');
});
