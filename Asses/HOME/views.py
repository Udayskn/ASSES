from HOME.models import Problem,Submission,TestCase
from django.views import generic
from django.shortcuts import render, redirect, get_object_or_404
from HOME.forms import CodeForm
from django.conf import settings
from django.http import HttpResponse
import docker,subprocess
import os.path
import time,os,signal
from time import time
# Create your views here.
class HomeView(generic.ListView):
    template_name = 'HOME/home.html'
    context_object_name = 'Problem_list'

    def get_queryset(self):
        return Problem.objects.all()
    
def ProblemView(request, problem_id):
    #template_name='HOME/problem.html'
    problem = get_object_or_404(Problem, id=problem_id)
    form = CodeForm()
    context = {
        'ProblemName': problem.name,
        'Problemstatement': problem.description,
        'problem_id': id,
        'problem': problem,
        'form' : form
    }
    return render(request, 'HOME\problem.html', context)

def VerdictView(request,problem_id):    
    if request.method == 'POST':
            # extract data from form
        form = CodeForm(request.POST)
        user_code = 'Not_valid'
        if  form.is_valid():
            instance = form.save(commit=False)
            user_code = form.cleaned_data.get('user_code')
            user_code = user_code.replace('\r\n','\n').strip()
            instance.problem = Problem.objects.get(id=problem_id)
            if request.user.is_authenticated:
                instance.user=request.user
            instance.save()
        else :
            print(form.errors)

        # user_code=request.POST['user_code']    
        language = request.POST['language']

        if request.method == 'POST':
            # setting docker-client
            docker_client = docker.from_env()
            Running = "running"
            problem = Problem.objects.get(id=problem_id)
            testcases = TestCase.objects.filter(problem_id=problem_id)
            filename=str(problem.id)
            # print(filename)
            if language == "C++":
                    extension = ".cpp"
                    cont_name = "oj-cpp"
                    compile = f"g++  {filename}.cpp"
                    clean = f" {filename}.cpp"
                    docker_img = "gcc:11.2.0"
                    exe = f"./{filename}.out"
            file = filename + extension
            filepath = os.path.join('HOME/Usercodes', file)
            code = open(filepath,"w")
            code.write(user_code)
            code.close()
            print("sending usercode to :"+filepath)
            # checking if the docker container is running or not
            try:
                container = docker_client.containers.get(cont_name)
                container_state = container.attrs['State']
                container_is_running = (container_state['Status'] == Running)
                if not container_is_running:
                    subprocess.run(f"docker start {cont_name}",shell=True)
            except docker.errors.NotFound:
                subprocess.run(f"docker run -dt --name {cont_name} {docker_img}",shell=True)
            res="Not compiled"
            verdict="Wrong Answer"
                # copy/paste the .cpp file in docker container 
            
            t=subprocess.run(f"docker cp {filepath} {cont_name}:/{file}",shell=True)
            # if(file):
                # print("q",file)
                # print("p",filepath)
                # subprocess.run(f"docker cp {filepath} {cont_name}:/{file}",shell=True)
            # compiling the code
            cmp = subprocess.run(f"docker exec {cont_name} {compile}", capture_output=True, shell=True)
            if(cmp):
                print("cmp",cmp)
            if cmp.returncode != 0:
                verdict = "Compilation Error"
                run_time="Not compiled"
                # subprocess.run(f"docker exec {cont_name} rm {file}",shell=True)

            else:
                for testcase in testcases :
                    #replacing \r\n by \n in original output to compare it with the usercode output
                    testcase.output = testcase.output.replace('\r\n','\n').strip() 
                    # running the code on given input and taking the output in a variable in bytes
                    start = time()
                    try:
                        begin=time()
                        res = subprocess.run( f'docker exec -it {cont_name} sh -c "echo \'{testcase.input}\' | ./a.out"' ,
                                                        capture_output=True, timeout=10,shell=True)
                        
                        run_time = time()-start
                        # res = subprocess.run(f" docker exec -it  {cont_name} sh -c "echo "5 4 3 2 1" | {exe}.out" ",
                        #                                 capture_output=True, timeout=100000, shell=True)
                        if(res):
                            print("result",res)
                        print("time",run_time)
                        subprocess.run(f"docker exec {cont_name} rm {clean}",shell=True)
                    except subprocess.TimeoutExpired:
                        run_time = time()-start
                        print("exceeded")
                        verdict = "Time Limit Exceeded"
                        subprocess.run(f"docker container kill {cont_name}", shell=True)
                        subprocess.run(f"docker start {cont_name}",shell=True)
                        subprocess.run(f"docker exec {cont_name} rm {clean}",shell=True)
                    if verdict != "Time Limit Exceeded" and res.returncode != 0:
                        verdict = "Runtime Error"
                    user_stderr = ""
                    user_stdout = ""
                    if verdict == "Compilation Error":
                        user_stderr = cmp.stderr.decode('utf-8')
                    
                    else:
                        verdict="Wrong Answer"
                        print("expected",testcase.output)
                        user_stdout = res.stdout.decode('utf-8')
                        print("useroutput",user_stdout)
                        if str(user_stdout)==str(testcase.output):
                            verdict = "Accepted"
                        testcase.output += '\n' # added extra line to compare user output having extra line at the end of their output
                        if str(user_stdout)==str(testcase.output):
                            verdict = "Accepted"
                    if verdict != "Accepted":
                        break
                instance.problem=problem
                instance.verdict=verdict
                instance.save()
                    

            
            
            print(instance)
            context={
            'Code': user_code,
            'lang': language,
            'res':res,
            'verdict':verdict,
            # 'user_stderr':user_stderr,
            # 'user_stdout': user_stdout,
            # 'time':run_time
            }
                    
    #return render(request, 'home\problemverdict.html', context)

    return HttpResponse('verdict:{}'.format(verdict)) # for debugging purpose.