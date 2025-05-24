import sys
import traceback
from pathlib import Path

# 最初にプロジェクトのルートディレクトリをパスに追加
sys.path.append(str(Path(__file__).parent.parent.parent))

from browser_use import BrowserConfig
from src.get_llm import LLMConfig
from src.entity.controller_type import ControllerType
from src.get_agent import get_agent
from typing import List


def execute_agent(
    instruction: str,
    llm_config: LLMConfig,
    browser_config: BrowserConfig,
    controller_types: List[ControllerType],
    output_dir: str,
):
    """
    エージェントを取得して実行します
    """
    try:
        # エージェントの取得
        agent = get_agent(
            instruction=instruction,
            llm_config=llm_config,
            browser_config=browser_config,
            controller_types=controller_types,
            output_dir=output_dir,
        )

        # エージェントの実行
        # agent.runは非同期関数である可能性があるので、適切に扱う
        try:
            import asyncio
            import inspect
            
            # agentのrunメソッドが非同期かどうかをチェック
            if inspect.iscoroutinefunction(agent.run):
                # 非同期関数の場合
                # すでに実行中のイベントループがあればそれを使用、なければ新規作成
                try:
                    loop = asyncio.get_running_loop()
                except RuntimeError:
                    loop = asyncio.new_event_loop()
                    asyncio.set_event_loop(loop)
                
                # 非同期関数を実行
                if loop.is_running():
                    # すでにイベントループが実行中の場合
                    result = asyncio.run_coroutine_threadsafe(agent.run(), loop).result()
                else:
                    # イベントループが実行中でない場合
                    result = loop.run_until_complete(agent.run())
            else:
                # 同期関数の場合は普通に実行
                result = agent.run()
                
            return result
        except AttributeError:
            # agent.runが存在しない場合
            error_msg = "Error: agent.run method not found"
            sys.stderr.write(error_msg + "\n")
            raise Exception(error_msg)
    except ImportError as e:
        error_msg = f"インポートエラー: {str(e)}\n{traceback.format_exc()}"
        sys.stderr.write(error_msg + "\n")
        raise e
    except Exception as e:
        error_msg = f"エージェント実行エラー: {str(e)}\n{traceback.format_exc()}"
        sys.stderr.write(error_msg + "\n")
        raise e
