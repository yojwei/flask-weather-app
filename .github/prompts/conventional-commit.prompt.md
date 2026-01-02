---
description: 'Prompt and workflow for generating conventional commit messages using a structured XML format. Guides users to create standardized, descriptive commit messages in line with the Conventional Commits specification, including instructions, examples, and validation.'
tools: ['runCommands/runInTerminal', 'runCommands/getTerminalOutput']
---

### Instructions

```xml
	<description>This file contains a prompt template for generating conventional commit messages. It provides instructions, examples, and formatting guidelines to help users write standardized, descriptive commit messages in accordance with the Conventional Commits specification.</description>
	<note>
```

### Workflow

**Follow these steps:**

1. Run `git status` to review changed files.
2. Run `git diff` or `git diff --cached` to inspect changes.
3. **Analyze and categorize changed files by their relationship:**
   - Group related changes together (e.g., feature files, bug fixes, documentation updates)
   - Identify dependencies between changes
   - Separate unrelated modifications into different groups
4. **For each group of related changes:**
   - Stage the files with `git add <file1> <file2> ...`
   - Construct the commit message using the XML structure below
   - Execute the commit command
5. After generating your commit message, Copilot will automatically run the following command in your integrated terminal (no confirmation needed):

```bash
git commit -m "type(scope): description"
```

6. **Repeat step 4-5 for each group** until all changes are committed.
7. Just execute this prompt and Copilot will handle the commits for you in the terminal sequentially.

### Commit Message Structure

```xml
<commit-message>
	<type>feat|fix|docs|style|refactor|perf|test|build|ci|chore|revert</type>
	<scope>()</scope>
	<description>A short, imperative summary of the change (使用繁體中文 zh_tw)</description>
	<body>(optional: more detailed explanation, 使用繁體中文 zh_tw)</body>
	<footer>(optional: e.g. BREAKING CHANGE: details, or issue references)</footer>
</commit-message>
```

### Examples

```xml
<examples>
	<example>feat(parser): add ability to parse arrays</example>
	<example>fix(ui): correct button alignment</example>
	<example>docs: update README with usage instructions</example>
	<example>refactor: improve performance of data processing</example>
	<example>chore: update dependencies</example>
	<example>feat!: send email on registration (BREAKING CHANGE: email service required)</example>
</examples>
```

### Validation

```xml
<validation>
	<type>Must be one of the allowed types. See <reference>https://www.conventionalcommits.org/en/v1.0.0/#specification</reference></type>
	<scope>Optional, but recommended for clarity.</scope>
	<description>Required. Use the imperative mood (e.g., "add", not "added"). 必須使用繁體中文 (zh_tw)。</description>
	<body>Optional. Use for additional context. 若有內容則必須使用繁體中文 (zh_tw)。</body>
	<footer>Use for breaking changes or issue references.</footer>
</validation>
```

### Final Step

```xml
<final-step>
	<analysis>
		<instruction>分析所有變更的檔案，依照以下原則進行分類：</instruction>
		<grouping-rules>
			<rule>相同功能或特性的變更歸為一組</rule>
			<rule>修復同一個問題的變更歸為一組</rule>
			<rule>相同模組或元件的變更歸為一組</rule>
			<rule>文件更新與程式碼變更分開</rule>
			<rule>配置檔案變更與功能變更分開</rule>
		</grouping-rules>
	</analysis>
	<sequential-commits>
		<instruction>對每一組相關的變更依序執行以下命令：</instruction>
		<step1>git add [相關檔案列表]</step1>
		<step2>git commit -m "type(scope): description"</step2>
		<note>Replace with your constructed message. Include body and footer if needed.</note>
		<note>重複此流程直到所有變更都已提交</note>
	</sequential-commits>
</final-step>
```
