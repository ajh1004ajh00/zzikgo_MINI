import os
import asyncio

from google.adk.agents import Agent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.adk.artifacts.in_memory_artifact_service import InMemoryArtifactService
from google.genai import types
from toolbox_core import ToolboxSyncClient

# 환경변수에 발급받은 Google API 키 설정
os.environ['GOOGLE_API_KEY'] = os.getenv('GOOGLE_API_KEY', 'your-api-key')

async def main():
    with ToolboxSyncClient("http://127.0.0.1:5000") as tc:
        tools = tc.load_toolset("user-toolset")

        agent = Agent(
            model='gemini-2.0-flash-001',
            name='user_agent',
            description='A helpful assistant for full user CRUD operations',
            instruction="""
You have these tools available (exact names & parameters):

1) create-user(platform_id: string, platform_user_id: string)
   - Creates a new user. id and created_at, max_storage_mb are generated automatically.
   Example call:
   {"tool": "create-user", "args": {"platform_id": "P_123", "platform_user_id": "alice"}}

2) search-user(query: string)
   - Finds existing users by id or platform_user_id.
   Example call:
   {"tool": "search-user", "args": {"query": "alice"}}

3) search-users-by-date(date: string)
   - Finds users created after the given ISO date.
   Example call:
   {"tool": "search-users-by-date", "args": {"date": "2025-07-01"}}

4) update-user-storage(id: string, max_storage_mb: integer)
   - Updates the max_storage_mb for a user.
   Example call:
   {"tool": "update-user-storage", "args": {"id": "U_abc", "max_storage_mb": 2048}}

5) delete-user(id: string)
   - Deletes a user by id.
   Example call:
   {"tool": "delete-user", "args": {"id": "U_abc"}}

When you receive a user request, **directly** call the appropriate tool with JSON args as above. Do not respond in plain text or ask for extra confirmation.
""",
            tools=tools,
        )

        session_svc = InMemorySessionService()
        art_svc     = InMemoryArtifactService()
        session = await session_svc.create_session(
            state={}, app_name='user_agent', user_id='tester'
        )

        runner = Runner(
            app_name='user_agent',
            agent=agent,
            artifact_service=art_svc,
            session_service=session_svc,
        )

        print("종료하려면 빈 줄(엔터)만 입력하세요.\n")
        while True:
            query = input("질문을 입력하세요: ").strip()
            if not query:
                print("프로그램을 종료합니다.")
                break

            content = types.Content(role='user', parts=[types.Part(text=query)])
            events = runner.run(
                session_id=session.id,
                user_id='tester',
                new_message=content
            )

            for event in events:
                # event.content가 None일 수 있으니 확인 후 처리
                if event.content and event.content.parts:
                    for part in event.content.parts:
                        if part.text:
                            print("→", part.text)
            print()  # 한 쿼리당 여백 한 줄

if __name__ == "__main__":
    asyncio.run(main())
