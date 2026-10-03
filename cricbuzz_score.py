
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError


URL = "https://www.cricbuzz.com/"
SCREENSHOT = "score.png"

# Replace this with the selector you verify in Cricbuzz DevTools.
# Example selectors may change when Cricbuzz updates its website.
SCORE_SELECTOR = "div.cb-col.cb-col-100.cb-scrs-wrp"


def main():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)

        page = browser.new_page(
            viewport={"width": 1440, "height": 900}
        )

        try:
            print("Opening Cricbuzz...")
            page.goto(URL, wait_until="domcontentloaded", timeout=30000)

            # Wait for the score area instead of using sleep().
            # Playwright waits until the element actually appears.
            try:
                score_element = page.locator(SCORE_SELECTOR).first

                score_element.wait_for(
                    state="visible",
                    timeout=15000
                )

                score = score_element.inner_text().strip()

                if score:
                    print("\nLatest score:")
                    print(score)

                    page.screenshot(
                        path=SCREENSHOT,
                        full_page=True
                    )

                    print(f"\nScreenshot saved as: {SCREENSHOT}")

                else:
                    print("No live score found.")

            except PlaywrightTimeoutError:
                print("No live match/score found on Cricbuzz.")

                # Still save a screenshot so we can see the page state.
                page.screenshot(
                    path=SCREENSHOT,
                    full_page=True
                )

                print(f"Screenshot saved as: {SCREENSHOT}")

        except Exception as error:
            print(f"Error while opening Cricbuzz: {error}")

        finally:
            browser.close()


if __name__ == "__main__":
    main()