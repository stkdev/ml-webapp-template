<script>
    import { marked } from 'marked';

    let value = 'Markdwonで構成された短いサンプル文章を作成してください。ただし#が一つの見出しは使用せず#が3個以上の見出しを使用してください。';

    let inputMessage = '';
    let responseMessage = '';
    let resp_claude3 = '';
    let resp_gemini = '';

    async function sendMessage() {
        try {
            const response = await fetch('http://localhost:8000/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ message: value })
            });

            const data = await response.json();
            responseMessage = data;
            resp_claude3 = data.message_claude;
            resp_gemini = data.message_gemini;
        } catch (error) {
            responseMessage = 'Error: Unable to send message';
            console.error(error);
        }
    }

    function handleSubmit(event) {
        event.preventDefault();
        sendMessage();
    }

</script>

<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@picocss/pico@2/css/pico.min.css" />

<h2>Claud3, Geminiへの問い合わせサンプル</h2>

<p>通常はTailwindCSSを使ってデザインする想定ですが、このページではpicoを読み込んで表示させています。</p>

<div class="grid">
    input
    <textarea bind:value></textarea>

    preview
    <div>{@html marked(value)}
        <form on:submit={handleSubmit}>
            <button type="submit">Send</button>
        </form>
    </div>

    response:
    {#if responseMessage}
        <div class="resp">
            <div>
                <h1>Claud3:</h1>{@html marked(resp_claude3)}
            </div>
            <div>
                <h1>Gemini:</h1>{@html marked(resp_gemini)}
            </div>
        </div>
    {/if}

</div>

<style>
    .grid {
        display: grid;
        grid-template-columns: 5em 1fr;
        grid-template-rows: 1fr 1fr;
        grid-gap: 1em;
        height: 100%;
    }

    textarea {
        flex: 1;
        resize: none;
    }

    form {
        margin-bottom: 1em;
    }

    div.resp {
        max-height: 300px;
    }

</style>
