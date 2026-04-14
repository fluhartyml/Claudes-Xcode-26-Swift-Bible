## 13. Submitting to the App Store

At this point you have a working app. It builds, runs on your phone, and does what it says on the tin — browses the web, saves bookmarks, and shares pages. That's the easy part. Getting it onto the App Store is a separate skill, and the first time you do it, something will go wrong. The submission walked through in this section went wrong in three different ways before it finally took — a name collision and two whitespace rejections — and all three are recorded here on purpose. A sanitized "click Submit and wait" walkthrough would not prepare you for what actually happens.

One thing to keep in mind throughout this section: the app has three different names, and they do not all change together.

- The **Xcode project name** is `Wraply`. That's what you see in the Navigator and in folder paths on disk. It does not change.
- The **Bundle Identifier** is `com.ClaudeX26Bible.Wraply`. That's Apple's internal unique ID for the app. It does not change either.
- The **Display Name** is what shows under the app icon on the home screen and on the App Store listing. Originally that was `Wraply` too — but "Wraply" was already taken on the App Store, so we changed the Display Name to `Claude's Web Wrapper` while leaving the project name and bundle ID alone.

Every time this section uses the word "Wraply," it means the internal project name. Every time it uses "Claude's Web Wrapper," it means the storefront name. They refer to the same app.

> **Building this to publish?** Keeping your Xcode project named Wraply is fine — that's internal and doesn't conflict with anything. But **do not** submit your build to the App Store with "Wraply" or "Claude's Web Wrapper" as the Display Name. Both are already claimed. Pick your own Display Name before you archive, the same way Apple forced us to pick one. Your bundle identifier will be different from ours anyway (it uses your Organization Identifier from Section 1.3), so Apple sees it as a distinct app — just give it a distinct name too.

13.1 Before you archive, open the project settings and check a handful of values. Here is how you get there:

- In the **Project Navigator** (the leftmost sidebar, the folder-tree icon — or press **Cmd+1**), click the very top entry: the blue Xcode project icon labeled **Wraply**. Not the folder below it, the blue icon.
- The center of the window changes. At the top you will see two columns of headings: **PROJECT** (with "Wraply" under it) and **TARGETS** (with "Wraply" under it as well). Click the **Wraply** under **TARGETS**.
- Now a row of tabs appears across the top of the editor: **General**, **Signing & Capabilities**, **Resource Tags**, **Info**, **Build Settings**, **Build Phases**, **Build Rules**, **Package Dependencies**. Click **General**. This is "the General tab." Every time the book says "go to the General tab," this is where it means.

**[Fig. W.19 — General tab with Display Name and Bundle Identifier visible]**

Check these values on the General tab:

- **Display Name:** Claude's Web Wrapper
- **Bundle Identifier:** com.ClaudeX26Bible.Wraply (or yours)
- **Version:** 1.0
- **Build:** 1
- **Minimum Deployments:** iOS 17.0 (SwiftData requires it)
- **Supported Destinations:** iPhone, iPad

13.2 Set the scheme to **Any iOS Device (arm64)** in the top bar of Xcode (between the Run/Stop buttons and the status area). You cannot archive with a simulator selected — the archive command will be grayed out.

13.3 **Product > Archive**. Xcode builds the release version and opens the **Organizer** window when done. The Organizer is where your archives live. At the top of the Archives tab you will see your new archive: **Wraply**, **1.0 (1)**, today's date, iOS App Archive. On the right side of the window you will see two action buttons: **Distribute App** and **Validate App**.

**[Fig. W.20 — Organizer window with freshly archived Wraply 1.0 (1)]**

13.4 Click **Validate App** — not Distribute App. Validate App is a pre-flight check that talks to Apple's servers and verifies that your archive is ready to submit: signing is valid, the bundle ID is registered, assets are correct, and — critically — the display name is available. Running Validate first is cheaper than running Distribute. If something is wrong, Validate tells you in a minute or two, before you have committed to uploading a gigabyte of binary.

A dialog opens titled **Select a method for validation:** with two options — **Validate** (recommended, uses default App Store Connect settings) and **Custom**. Leave Validate selected and click the **Validate** button in the bottom right.

**[Fig. W.21 — Select a method for validation dialog]**

13.5 Xcode shows a form titled **Validate with App Store Connect** with this message: "Your app must be registered with App Store Connect before it can be uploaded. Xcode will create an app record with the following properties."

Below the message you will see four fields, auto-populated (some editable, some locked):

- **Name:** Wraply
- **SKU:** com.ClaudeX26Bible.Wraply
- **Primary Language:** English (United States)
- **Bundle Identifier:** com.ClaudeX26Bible.Wraply

Some of these fields are editable right there in the dialog. **Name** and **SKU** can be retyped; **Primary Language** has a dropdown. **Bundle Identifier** is locked — it is read directly from your archive's Info.plist and cannot be changed here. The Name field is the one that will be used as your App Store listing name. Xcode pre-fills it with your target name — which is Wraply.

**[Fig. W.22 — Validate form: Name field populated with "Wraply"]**

13.6 Click **Next**. Xcode talks to Apple's servers for a few seconds, then stops and shows you a red X and this error:

**App Record Creation Error** — App Record Creation failed due to request containing an attribute already in use. The App Name you entered is already being used. If you have trademark rights to this name and would like it released for your use, submit a claim.

Someone else has the name "Wraply" on the App Store. You cannot use it, and Apple caught it here at the pre-flight stage rather than two days from now in Review.

**[Fig. W.23 — App Record Creation Error: name already in use]**

This is the first **Teaching Moment** of the submission. Apple's pre-flight catches the name collision here rather than after a full upload. If you had clicked Distribute first instead of Validate, you would have gone through the whole upload flow — minutes of signing and pushing bytes — only to hit this same error at the end. That's why you Validate first.

13.7 Click **Cancel** to get out of the Validate flow. You need to change the Display Name. Go back to Xcode, click the blue Wraply project icon, click the Wraply target, go to the **General** tab (from Section 13.1), and find the **Display Name** field under the **Identity** section. Change it from **Wraply** to **Claude's Web Wrapper**.

We picked **Claude's Web Wrapper** because this app ships as a companion to Claude's X26 Swift6 Bible — tying the storefront name to the book and its author (Claude) kept the branding consistent. When you do this for your own app, the only rule is that the display name you pick must not already be taken on the App Store.

While you're here, you can also check the **App Category** picker in the same Identity section. Set it to something reasonable; we will lock it in on the App Store Connect side later too. For a web browser / source code viewer, Education is the strongest choice. Books is tempting — this *is* a book companion — but Apple reads "Books" as "ebook reader or library" and tends to reject under Guideline 4.2 Minimum Functionality when the category does not match the content. We talked ourselves out of Books before the first submission attempt, and you should too.

**[Fig. W.24 — Xcode General tab: Display Name updated to "Claude's Web Wrapper"]**

13.8 Re-archive the project. **Product > Archive** again. Changing the Display Name invalidates the existing archive — the old archive still has "Wraply" baked into its metadata, and Xcode will happily let you validate it and hit the same error again. A fresh archive picks up the new Display Name.

When the archive completes, the Organizer opens with both archives listed — the old one (still named Wraply) and the new one (still named Wraply on the archive row, because the archive row shows the *target* name, which hasn't changed). Click the newest archive. The action buttons — Distribute App and Validate App — come back up on the right.

Click **Validate App**. Select the Validate method. Click Validate.

13.9 The **Validate with App Store Connect** form appears again. Check the Name field.

It still says **Wraply**.

This is the single most important thing to know about submitting to the App Store. The Display Name you set in the General tab does **not** automatically flow into the Name field of the Validate or Distribute dialog. The dialog pre-fills its Name field from the target name (which is still "Wraply"), not from the Display Name. You have to change it here too.

**[Fig. W.25 — Validate form: Name still auto-populates as "Wraply"]**

> **The trap you will fall into.** The first time this happens, you will assume something didn't save. You will close the dialog, go back to General, confirm that Display Name really does say Claude's Web Wrapper, re-type it anyway, re-archive, open Organizer, click Validate, watch "Wraply" reappear in the Name field, and start to lose your mind. Maybe you delete the old archive thinking it's stale. Maybe you clean the build folder. None of it helps. The Organizer fills up with stacked "Wraply 1.0 (1)" archives from every re-attempt — none of them are wrong, they just were not the problem.

**[Fig. W.25b — Multiple Wraply archives stacking in the Organizer from re-archive attempts]**

> **Tip: use the Build number as an archive label.** Before each re-archive, bump the **Build** field in the General tab by one (1 → 2 → 3 → ...). The Organizer shows the build number alongside each archive, so 1.0 (1), 1.0 (2), 1.0 (3) become visually distinct rows. You can then tell at a glance which archive is the newest, click it, and right-click → Delete on the older ones without wondering which is which. Apple doesn't care about gaps in your build numbers — they only care that a build number isn't reused.
> The Name field is not reading from anywhere you can change outside this dialog. **The only fix is to type the new name into this Name field, every single time you run Validate or Distribute, until your submission is accepted.** That is the bug. It is not your fault, and you are not missing a setting somewhere.

13.10 Click inside the Name field. Select the whole word "Wraply" and delete it. The field will show just a cursor.

**[Fig. W.26 — Name field mid-edit: backspaced down to "W"]**

13.11 Type **Claude's Web Wrapper**. Press **Tab** to move focus to the next field and commit the change. Do not press Enter — that may submit the form prematurely on some systems.

**[Fig. W.27 — Name field: "Claude's Web Wrapper" typed cleanly]**

> **Whitespace warning.** If you are backspacing and retyping fast, you can easily leave an invisible leading or trailing space in the Name field. You will not see it. Apple's pre-flight validator doesn't always catch it either. What happens later is that your build uploads successfully, Apple starts processing it, and then emails you an **ITMS-90694: Invalid bundle display name** rejection and your build silently disappears from App Store Connect. This is covered in detail below — but you can avoid it here by clearing the field completely with **Cmd+A Delete**, retyping cleanly, and then clicking somewhere else in the dialog to blur the field before clicking Next.

13.12 Click **Next**. Xcode shows a progress dialog labeled **Validate with App Store Connect** with the status **Preparing — Locating signing assets...** This step can take anywhere from ten seconds to a minute. Let it run.

**[Fig. W.28 — Preparing, Locating signing assets]**

13.13 When validation finishes, the dialog shows a green check and the message **App validation complete: Wraply 1.0 (1) validated. Your app successfully passed all validation checks.** Click **Done**.

**[Fig. W.29 — App validation complete: Wraply 1.0 (1) validated]**

The internal name "Wraply" still appears in this message. That is fine. The validation is about the archive (which is named Wraply on disk) and the bundle identifier, not the display name. Your Claude's Web Wrapper display name is registered with App Store Connect; that's what matters.

13.14 Now you can upload. Click **Distribute App** in the Organizer. A dialog appears titled **Select a method for distribution:** with six icons: **App Store Connect**, **TestFlight Internal Only**, **Release Testing**, **Enterprise**, **Debugging**, **Custom**.

Click **App Store Connect** and then click the **Distribute** button in the bottom right.

**[Fig. W.30 — Select a method for distribution: App Store Connect]**

13.15 Xcode shows a progress dialog labeled **Upload for App Store Connect** with the status **Processing — Signing Wraply.app...** followed by upload progress. This step takes one to three minutes depending on your connection speed and the size of the build.

**[Fig. W.31 — Processing, Signing Wraply.app]**

13.16 When the upload finishes, the dialog shows a green check and the message **App upload complete: Wraply 1.0 (1) uploaded**. Click **Done**.

**[Fig. W.32 — App upload complete: Wraply 1.0 (1) uploaded]**

Your archive is now on Apple's servers. The rest of the submission happens in the browser, at **appstoreconnect.apple.com**.

13.17 Open a browser and go to **appstoreconnect.apple.com**. Log in with your Apple Developer account. Click **Apps** in the top navigation. You will see a grid of app tiles — any apps you have previously submitted, plus the one you just created.

**Claude's Web Wrapper** should be in the grid with a status badge saying **iOS 1.0 — Prepare for Submission**. The app icon slot will be empty (a wireframe placeholder) because the uploaded build hasn't been processed yet.

**[Fig. W.33 — App Store Connect Apps list with Claude's Web Wrapper]**

13.18 Click **Claude's Web Wrapper** to open the app page. You will see a left sidebar with sections (App Information, Pricing and Availability, App Privacy, Age Rating, App Review) and a main content area for the iOS 1.0 version page. Work through the fields:

- **Promotional Text** (170 character maximum, can be updated without resubmitting): `Claude's Web Wrapper — browse the web, save bookmarks, and explore the app's own Swift source code. Companion app for Claude's X26 Swift6 Bible.`
- **Description** (4000 character maximum): `A web browser built as a companion app for Claude's X26 Swift6 Bible. Browse any website, save bookmarks, and share pages. Under the Hood lets you read and copy every Swift source file — paste into Xcode and learn by building. Educational tool for iOS development.`
- **Keywords** (100 character maximum total, comma-separated with **no spaces** after the commas): `swift,xcode,learn,code,browser,bookmark,source,education,ios,development`
- **Support URL:** `https://fluharty.me/projects/swift-bible.html` (or your own page)
- **Marketing URL:** optional, leave blank
- **Version:** 1.0
- **Copyright:** 2026 Michael Fluharty (or your name)

**[Fig. W.34 — iOS 1.0 Version page with promotional text, description, keywords filled in]**

13.19 Scroll down to the **Build** section of the iOS 1.0 page. If your upload has finished processing, you will see a **+ Add Build** button or a dropdown listing your build. Click it, select **1.0 (1)**, answer the **Encryption** compliance prompt (**None of the algorithms mentioned above**), and confirm.

If the Build section is still empty — just the sentence "Upload your builds using one of several tools" — processing has not finished yet. Normal processing time is under ten minutes.

**If processing takes more than thirty minutes, something is wrong.** Apple does not show processing failures in App Store Connect. They email you. Switch to your inbox. This is the second **Teaching Moment**: a build that does not appear is never a build that is "still processing." It is a build that was silently rejected by email.

**[Fig. W.35 — Build section empty after a long wait: something is wrong]**

13.20 Check your email. If there is a message from **App Store Connect** titled "Apple Developer Relations" about your build, open it. The body tells you the exact failure.

In this submission, the message read:

> **ITMS-90694: Invalid bundle display name** — `' Claude's Web Wrapper '` starts with a whitespace character.

The leading and trailing quote marks in the message are Apple's way of showing you what the display name looks like — including whitespace. The space before the `C` is a leading space that snuck into the Name field during the backspace-and-retype in Section 13.10. You didn't see it when you typed. Apple's validator didn't catch it during pre-flight validation either — that check looks at the Name value being sent, but a leading space is a legal string. The silent rejection happens later, at the bundle processing stage.

**[Fig. W.36 — ITMS-90694 rejection email: whitespace in display name]**

> **The invisible whitespace problem.** Typing names into validation dialogs is fragile. When you backspace through an auto-populated value and retype, the field can end up with a leading or trailing space from before the first character or after the last one. You will never see it on screen. App Store Connect will never show you the error in its UI. The build will upload, pass its quick pre-flight, start processing, and then silently vanish from the Build dropdown while Apple emails you. The rule is: always check your inbox when a build hasn't appeared in App Store Connect within thirty minutes.

13.21 Back in Xcode, fix the whitespace. Go to the **General** tab, click inside the **Display Name** field, press **Cmd+A** to select everything, **Delete** to clear, then type **Claude's Web Wrapper** fresh. Click anywhere outside the field to commit. Also bump the **Build** number from **1** to **2** — you cannot re-upload the same build number, and Apple tracks build numbers strictly.

If you re-archive and hit the same ITMS-90694 whitespace rejection again, you likely still have an invisible trailing space. The real submission documented here hit this loop twice. At one point the problem looked like it might be the apostrophe in "Claude's" — special characters in display names have been known to cause trouble — but stripping the apostrophe to try "Claudes Web Wrapper" did not fix it either. The actual cause was always a stray space. The fix is always the same: clear with **Cmd+A Delete**, type cleanly, tab out, archive. Slow down.

> **Do not delete the app record from App Store Connect to "reset" things.** When a submission is stuck, it is tempting to open App Store Connect, delete the app record, and try again from Xcode thinking a clean slate will fix it. It will not. Apple tracks deleted records by bundle identifier. Once your bundle ID is tied to a record in **Removed Apps** state, any new Validate or Distribute attempt comes back with "App record with bundle identifier ... was previously removed from App Store Connect. Go to App Store Connect to restore the app." The only fix is in the web: **Apps → filter Removed Apps → click your app → Restore**. Then retry Validate. Leave the app record alone until the submission is through review.

**[Fig. W.37 — The "previously removed" error, triggered by deleting the app record]**

> **The nuclear option.** If the submission has completely collapsed — bundle ID tangled, nothing you try in Validate works, Restore doesn't help — you can start fresh: create a new Xcode project with a different Product Name (giving you a new Organization Identifier + Product Name combination, and therefore a fresh bundle ID), copy your source files over, and submit that. It's a hard reset, and you lose your prior archive history, but it always works. We planned on this as the fallback during the real submission and didn't end up needing it.

13.22 Back in the Organizer, with your Build 2 archive selected, click **Validate App**. Pick the Validate method, fill in the Name field cleanly (**Claude's Web Wrapper**), and click **Next**. Validation completes: **Wraply 1.0 (2) validated**. Click Done. Then click **Distribute App**, choose **App Store Connect**, click Distribute. Xcode signs and uploads Build 2.

When the upload dialog reports **App upload complete: Wraply 1.0 (2) uploaded**, you are done in Xcode for this submission.

**[Fig. W.38 — Build 2 uploaded successfully]**

13.23 In the upload-complete dialog, below the green check, you'll see the text **Show in App Store Connect** with a small **arrow-in-a-circle** icon next to it. Click that icon. It launches your default web browser, opens **appstoreconnect.apple.com**, and prompts you to log in with your Apple Developer account if you aren't already.

**[Fig. W.32b — App Store Connect login prompt after clicking the arrow link]** Once you're in, you land on your **Apps** grid — a tiled list of every app you've ever created in App Store Connect.

Find **Claude's Web Wrapper** in the grid. Its icon slot will be a wireframe placeholder because your app icon hasn't been processed as an App Store listing icon yet — that comes after the build is attached to the version. Click the tile.

**[Fig. W.33 — App Store Connect Apps grid: Claude's Web Wrapper tile with wireframe placeholder icon]**

You're now on the app's page. The default tab is **Distribution** — that's where you were headed. Wait a few minutes for Apple to finish processing Build 2; this time processing should succeed because the whitespace is fixed and the app record has been restored. You'll get a **"The following build has completed processing"** email when it's ready.

13.24 Scroll down to the **Build** section of the iOS 1.0 page. If processing has completed, you will see the **+ Add Build** button (a small blue circle with a plus sign) next to the section title, and an **Add Build** button inside the section.

**[Fig. W.38b — iOS App Version 1.0 page: Build section with + Add Build button visible]**

> **If the Add Build button doesn't appear**, App Store Connect is holding onto unsaved edits. Scroll up, click **Save** in the top right of the page to commit everything you've typed so far (promotional text, description, keywords, screenshots — none of it is saved automatically), then **reload the page in your browser**. The + Add Build button should now be there. This is a pattern to remember: any time a button or status on an App Store Connect page seems to be missing, try Save → reload.

Click **+ Add Build**. A modal titled **Add Build** appears with a list of available builds and a note about encryption compliance. Pick **2** from the list.

**[Fig. W.39 — Add Build dialog: 1.0 (2) selected with "Missing Compliance" before answering encryption]**

13.25 Now fill in the remaining required sections in App Store Connect. In the left sidebar:

- **App Information** — set **Primary Category** to **Education**. Scroll to **Content Rights Information** and choose **This app does not contain, show, or access third-party content**. (If you pick Books, Apple reads it as "ebook reader or library" and tends to reject under Guideline 4.2 Minimum Functionality. Education is the safe choice for a companion app.)

**[Fig. W.39c — Content Rights Information: "No, it does not contain, show, or access third-party content"]**

- **Pricing and Availability** — set **Availability** first, then **Price**. If you set Price before Availability, the Availability wizard later asks you additional questions about where your pricing applies (including EU-specific requirements that vary by region), adding steps. Configuring Availability first lets you pick your regions cleanly, and the Price step then applies across that selection in one pass.
  - **App Availability** → click **Set Up Availability** → choose **Specific Countries or Regions** and select **United States** and **Canada** first. Skip the European Union, United Kingdom, and other regions on your first submission. Those regions have their own legal compliance requirements (GDPR data processing disclosures, EU Digital Services Act, digital service taxes in some countries) that are better dealt with as a follow-up once your app is live in North America. You can always extend availability to more regions later from the same page, without resubmitting.
  - **Price Schedule** → click **Add Pricing** → choose **Free** (or your tier). The tier applies across the countries you selected.

**[Fig. W.39d — Pricing and Availability page after selecting US and Canada: App Availability shows "2 Available, 173 Not Available"]**

- **App Privacy** — enter a **Privacy Policy URL**. You need one even if your app collects nothing. A page on your portfolio that says the app does not collect personal data is enough.

**[Fig. W.39e — App Privacy page with Privacy Policy URL filled in (fluharty.me/privacy) and "Data Not Collected"]**

- **Age Rating** — answer every question **No** for this app; you land at **4+**.

**[Fig. W.39f — Age Ratings wizard: answering content questions (e.g. Violence step — all None)]**

- **App Review Information** — scroll to the bottom of the iOS 1.0 Version page. This section has two important parts:
  - **Sign-In Information** — this is a **radio button selector**. The **Sign-in required** option is selected by default. If your app does not require users to sign in (Claude's Web Wrapper does not — it has no accounts), verify that Sign-in required is **not** selected before you submit. If it stays selected, the reviewer will expect a test username and password in your notes; when they don't find one, the app gets rejected.
  - **Contact Information** — fill in first name, last name, phone, and email. Notes are optional — put anything a reviewer should know (test credentials if sign-in is required, unusual features, permissions explanations).

**[Fig. W.39g — App Review Information: Sign-in required radio deselected, Contact Information filled in]**

13.26 Scroll up to the top of the iOS 1.0 page. You also need **Screenshots**. Find the **App Preview and Screenshots** section. Apple requires screenshots for every display size your app supports. For a universal iPhone + iPad app, the minimum is one **6.5" iPhone Display** (1284 × 2778) screenshot and one **13" iPad Display** screenshot.

Upload the four iPhone screenshots you captured in Section 12 into the **iPhone 6.5" Display** slot.

For the **13" iPad Display** slot, App Store Connect will block your submission if it's empty — and it will **not** accept your iPhone-aspect screenshots in the iPad slot (the upload gets rejected for wrong dimensions). You have two real options:

1. **Capture iPad simulator screenshots.** Boot an iPad simulator in Xcode (for example iPad Pro 13"), run the app, press **Cmd+S** in the simulator to save a screenshot, repeat for the scenes you want (browser, Under the Hood, source viewer, share sheet). Upload those into the iPad slot.
2. **Disable iPad compatibility in Xcode.** Go to the project's General tab (Section 13.1), find **Supported Destinations**, and remove **iPad**. Re-archive, upload a new build, and submit as iPhone-only. App Store Connect then drops the iPad screenshot requirement entirely.

Option 1 is the right call if you want your app on iPad. Option 2 is the right call if you have not tested on iPad and don't want to ship something half-finished there. Picking option 2 and then adding iPad support in a later version is a clean path.

**[Fig. W.39h — Previews and Screenshots with iPhone 6.5" Display populated: 4 screenshots of Claude's Web Wrapper visible, iPad tab also available]**

13.27 Click **Add for Review** in the top right. App Store Connect checks your submission and shows you a modal listing anything still missing. Common ones on a first submission:

- You must upload a screenshot for 13-inch iPad displays.
- You must complete the Contact Information section.
- You must enter a Privacy Policy URL in App Privacy.
- You must set up Content Rights Information in App Information.
- You must select a primary category for your app.

**[Fig. W.39b — "Unable to Add for Review" checklist listing remaining required items]**

Fix each one, scroll back up, click **Add for Review** again. Repeat until App Store Connect stops complaining.

13.28 When there are no more missing fields, **Add for Review** changes to **Submit for Review** (or a **Draft Submission** panel slides in from the right with a **Submit for Review** button at the bottom). Click it. Confirm the submission.

**[Fig. W.40b — Draft Submission panel: iOS App 1.0 (2) listed as "Ready to Submit" with Submit for Review button]**

The iOS 1.0 page now shows the status **Waiting for Review**. The Distribution tab shows the submission ID and the exact time you submitted. Apple's reviewers will look at your build, usually within 24 to 48 hours, and email you when it is approved or rejected.

**[Fig. W.40 — Waiting for Review, submission confirmed]**

---

**Learning moments from the Claude's Web Wrapper submission:**

1. **Validate App before Distribute App.** Validate is a cheap pre-flight. Distribute is a full upload. Run Validate first to catch name collisions, signing issues, and missing assets before you commit to an upload.
2. **Display Name in Xcode General does not flow into the Validate/Distribute Name field.** You must change it in both places. The Name field in the validation dialog auto-populates from the target name, which does not change.
3. **Whitespace is invisible and deadly.** Clearing with Cmd+A Delete, retyping cleanly, and tabbing out of the field is the only reliable way. Do not backspace.
4. **Processing rejections are silent in App Store Connect.** Apple emails them. If a build hasn't appeared in the Build dropdown within thirty minutes, check your inbox.
5. **Do not delete your app record in App Store Connect to reset a bad submission.** It leaves the bundle ID in a Removed Apps state and blocks any new submission until you restore the record.
6. **Books category triggers Guideline 4.2 (Minimum Functionality).** Pick Education for companion apps.

None of these are in Apple's documentation in any way you would find before hitting them. Now they are.
