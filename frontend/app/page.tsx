'use client';

import { useState, useEffect, useRef } from 'react';

export default function Home() {
	const [input, setInput] = useState('');
	const [messages, setMessages] = useState<
		{ role: 'user' | 'ai'; content: string }[]
	>([]);
	const [isLoading, setIsLoading] = useState(false);
	const messagesEndRef = useRef<HTMLDivElement>(null);

	const scrollToBottom = () => {
		messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
	};

	useEffect(scrollToBottom, [messages]);

	const handleSubmit = async (e: React.FormEvent) => {
		e.preventDefault();
		if (!input.trim() || isLoading) return;

		setMessages(prev => [...prev, { role: 'user', content: input }]);
		setInput('');
		setIsLoading(true);

		try {
			const response = await fetch('http://localhost:8000/stream', {
				method: 'POST',
				headers: {
					'Content-Type': 'application/json',
				},
				body: JSON.stringify({ input }),
			});

			if (!response.ok) {
				throw new Error('Network response was not ok');
			}

			const reader = response.body?.getReader();
			if (!reader) return;

			let aiResponse = '';
			setMessages(prev => [...prev, { role: 'ai', content: '' }]);

			while (true) {
				const { done, value } = await reader.read();
				if (done) break;

				const chunk = new TextDecoder().decode(value);
				const lines = chunk.split('\n\n');

				for (const line of lines) {
					if (line.startsWith('data: ')) {
						const data = JSON.parse(line.slice(6));
						if (data.content) {
							aiResponse += data.content;
							setMessages(prev => {
								const newMessages = [...prev];
								newMessages[newMessages.length - 1] = {
									role: 'ai',
									content: aiResponse,
								};
								return newMessages;
							});
						}
					}
				}
			}
		} catch (error) {
			console.error('Error:', error);
			//setMessages(prev => [
			//	...prev,
			//	{ role: 'ai', content: 'Error: Failed to get response' },
			//]);
		} finally {
			setIsLoading(false);
		}
	};

	return (
		<main className="flex min-h-screen flex-col items-center justify-between p-24">
			<div className="z-10 w-full max-w-5xl items-center justify-between font-mono text-sm">
				<h1 className="text-4xl font-bold mb-8">AI Rate My Professor</h1>
				<div className="bg-white p-4 rounded-lg shadow-md">
					<div className="h-96 overflow-y-auto mb-4">
						{messages.map((msg, index) => (
							<div
								key={index}
								className={`mb-4 ${
									msg.role === 'user' ? 'text-right' : 'text-left'
								}`}
							>
								<span
									className={`inline-block p-2 rounded-lg ${
										msg.role === 'user'
											? 'bg-blue-500 text-white'
											: 'bg-gray-200 text-gray-900'
									}`}
								>
									{msg.content}
								</span>
							</div>
						))}
						<div ref={messagesEndRef} />
					</div>
					<form onSubmit={handleSubmit} className="flex">
						<input
							type="text"
							value={input}
							onChange={e => setInput(e.target.value)}
							className="flex-grow p-2 border rounded-l-md text-gray-900 bg-white"
							placeholder="Type your message..."
							disabled={isLoading}
						/>
						<button
							type="submit"
							className={`p-2 rounded-r-md ${
								isLoading
									? 'bg-gray-400 cursor-not-allowed'
									: 'bg-blue-500 hover:bg-blue-600'
							} text-white`}
							disabled={isLoading}
						>
							{isLoading ? 'Sending...' : 'Send'}
						</button>
					</form>
				</div>
			</div>
		</main>
	);
}
