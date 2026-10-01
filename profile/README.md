<a href="https://sent.dm">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/sentdm/.github/main/profile/assets/hero-dark.svg">
    <source media="(prefers-color-scheme: light)" srcset="https://raw.githubusercontent.com/sentdm/.github/main/profile/assets/hero-light.svg">
    <img alt="Sent: one API for SMS, WhatsApp and RCS" src="https://raw.githubusercontent.com/sentdm/.github/main/profile/assets/hero-light.svg" width="100%">
  </picture>
</a>

<p align="center">
  <a href="https://app.sent.dm"><b>Get an API key</b></a>
  &nbsp;·&nbsp;
  <a href="https://docs.sent.dm">Docs</a>
  &nbsp;·&nbsp;
  <a href="https://docs.sent.dm/reference/api/test-mode">Sandbox mode</a>
  &nbsp;·&nbsp;
  <a href="https://status.sent.dm">Status</a>
  &nbsp;·&nbsp;
  <a href="https://x.com/sentdm">X</a>
  &nbsp;·&nbsp;
  <a href="https://www.linkedin.com/company/sentdm/">LinkedIn</a>
</p>

<br>

### Send your first message

Every send below runs with `sandbox: true`: the API validates and simulates the request, delivers nothing and spends no credits. Works on a brand-new account.

```bash
npm install @sentdm/sentdm
export SENT_DM_API_KEY="your-api-key"
```

```ts
import Sent from "@sentdm/sentdm";

const sent = new Sent(); // reads SENT_DM_API_KEY

await sent.messages.send({
  to: ["+15555550100"],
  text: "Hello from Sent",
  sandbox: true,
});
```

Leave `channel` out and Sent picks SMS, WhatsApp or RCS per recipient from your routing rules. Name one to pin it.

### Official SDKs

| Language | Install | Repo |
| :-- | :-- | :-- |
| TypeScript | `npm install @sentdm/sentdm` | [sent-dm-typescript](https://github.com/sentdm/sent-dm-typescript) |
| Python | `pip install sentdm` | [sent-dm-python](https://github.com/sentdm/sent-dm-python) |
| Go | `go get github.com/sentdm/sent-dm-go` | [sent-dm-go](https://github.com/sentdm/sent-dm-go) |
| Java / Kotlin | `dm.sent:sent-java` on [Maven Central](https://central.sonatype.com/artifact/dm.sent/sent-java) | [sent-dm-java](https://github.com/sentdm/sent-dm-java) |
| C# / .NET | `dotnet add package Sentdm` | [sent-dm-csharp](https://github.com/sentdm/sent-dm-csharp) |
| PHP | `composer require sentdm/sent-dm-php` | [sent-dm-php](https://github.com/sentdm/sent-dm-php) |
| Ruby | `gem install sentdm` | [sent-dm-ruby](https://github.com/sentdm/sent-dm-ruby) |

### Build with agents and automation

- [**sent-plugin**](https://github.com/sentdm/sent-plugin): Agent Skills plus an MCP server, so Claude Code, Codex and other agents can send, track and debug messages. `npx skills add https://github.com/sentdm/sent-plugin --skill sent`
- [**n8n-nodes-sent**](https://github.com/sentdm/n8n-nodes-sent): the Sent node for n8n workflows.

<br>

<p align="center">
  <sub>Building something on Sent? <a href="https://github.com/sentdm/.github/issues">Tell us</a>, we read every one.</sub>
</p>
