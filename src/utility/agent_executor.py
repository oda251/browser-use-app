import sys
import traceback
from pathlib import Path

# 最初にプロジェクトのルートディレクトリをパスに追加
sys.path.append(str(Path(__file__).parent.parent.parent))

from src.entity.controller_type import OutputFormat
from browser_use import BrowserConfig
from src.get_llm import LLMConfig
from src.get_agent import get_agent
from src.component.common.global_cache import get_global
from typing import List
import asyncio
import inspect


def execute_agent(
    instruction: str,
    llm_config: LLMConfig,
    browser_profile: BrowserConfig,
    output_format: OutputFormat,
    output_dir: str,
):
    """
    エージェントを取得して実行します
    """
    try:
        try:

            def should_stop():
                return get_global("agent_stop_flag", False)

            agent = get_agent(
                instruction=instruction,
                llm_config=llm_config,
                browser_profile=browser_profile,
                output_format=output_format,
                output_dir=output_dir,
                should_stop=should_stop,  # 追加
            )
        except ValueError as ve:
            error_msg = f"エージェント初期化エラー: {str(ve)}\n{traceback.format_exc()}"
            sys.stderr.write(error_msg + "\n")
            raise ve
        except Exception as e:
            error_msg = f"エージェント初期化エラー: {str(e)}\n{traceback.format_exc()}"
            sys.stderr.write(error_msg + "\n")
            raise e

        try:

            async def run_with_stop():
                # stopフラグを監視しつつ実行
                run_task = asyncio.create_task(agent.run())
                while not run_task.done():
                    await asyncio.sleep(0.2)
                    if get_global("agent_stop_flag", False):
                        if hasattr(agent, "stop"):
                            await maybe_await(agent.stop())
                        break
                try:
                    return await run_task
                except Exception as e:
                    raise e

            async def maybe_await(val):
                if inspect.isawaitable(val):
                    return await val
                return val

            try:
                loop = asyncio.get_running_loop()
            except RuntimeError:
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
            if loop.is_running():
                result = asyncio.run_coroutine_threadsafe(
                    run_with_stop(), loop
                ).result()
            else:
                result = loop.run_until_complete(run_with_stop())
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
