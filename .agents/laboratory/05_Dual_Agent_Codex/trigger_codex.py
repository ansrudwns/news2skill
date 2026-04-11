import subprocess
import time
import sys
import tempfile
import shutil
import os
import difflib

sys.stdout.reconfigure(encoding='utf-8')

def audit_code_with_codex():
    print("🤖 [Gemini -> Codex] 듀얼 에이전트 브릿지 통신을 시작합니다...\n")
    
    workspace_dir = r"c:\Users\m8686\Desktop\settings\.agents\laboratory\05_Dual_Agent_Codex"
    original_target = os.path.join(workspace_dir, "buggy_script.py")
    
    # [Harness Level Isolation] 
    # 워크스페이스 직접 파괴를 방지하기 위해 타겟 파일을 임시 폴더로 이동 후 작업
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_target = os.path.join(temp_dir, "buggy_script.py")
        shutil.copy2(original_target, temp_target)
        print(f"🔒 대상 파일이 안전하게 임시 격리되었습니다: {temp_dir}")
        
        prompt = "Look at buggy_script.py. Fix the logic bug in `calculate_discount` (it blindly subtracts the percentage). Print a unified diff only; do not edit files."
        command = [
            "codex.cmd", 
            "exec",
            "--skip-git-repo-check"
        ]
    
        start_time = time.time()
        try:
            print(f"📡 송신 중인 명령어: {' '.join(command)}")
            print("⏳ Codex가 코드를 분석하고 패치를 제안하는 중입니다. (제한 시간 180초)...\n")
            
            # 격리된 임시 폴더(temp_dir)를 작업 디렉터리로 부여하고, stdin으로 프롬프트 주입
            result = subprocess.run(command, input=prompt, capture_output=True, text=True, check=True, timeout=180, cwd=temp_dir)
            
            elapsed = time.time() - start_time
            print(f"✅ [Codex 응답 완료] 소요 시간: {elapsed:.1f}초")
            
            # [Verify Isolation] 원본 파일이 해킹당하지 않았는지 확인
            with open(original_target, 'r', encoding='utf-8') as f:
                original_code = f.readlines()
            with open(temp_target, 'r', encoding='utf-8') as f:
                modified_code = f.readlines()
                
            diff = list(difflib.unified_diff(original_code, modified_code, fromfile="buggy_script_original.py", tofile="buggy_script_patched.py"))
            
            print("\n======== 📝 CODEX 로그 (Temp Env) ========")
            print(result.stdout)
            print("===================================\n")
            
            print("\n======== 🔍 안전 검증 Diff(원본 vs 패치 시도) ========")
            if not diff:
                print("🔹 패치 사항 없음 (Codex가 파일을 변경하지 않았습니다).")
            else:
                sys.stdout.writelines(diff)
            print("========================================================\n")
            
        except subprocess.TimeoutExpired as e:
            print(f"❌ Codex 실행이 시간 초과(180초)되었습니다: {e}")
        except subprocess.CalledProcessError as e:
            print("❌ Codex 실행 중 에러가 발생했습니다.")
            print(e.stderr)
            
    print("🧹 [Harness] 임시 디렉터리가 자동 폐기되었습니다.")

if __name__ == "__main__":
    audit_code_with_codex()
