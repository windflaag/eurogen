#!/usr/bin/env python3
import os, json, argparse, sys

class Curler:
  @staticmethod
  def curlFile(url):
    filename = "./build/" + url.split("/")[-1]
    if not os.path.exists(filename):
      os.system(f"curl -o {filename} {url}")
    return filename

class Console:
  @staticmethod
  def run(cmd):
    os.system(cmd)

class PosixCommander:
  @staticmethod
  def ls():
    return Console.run("ls")
    
  @staticmethod
  def clear():
    return Console.run("clear")

  @staticmethod
  def rm(files):
    return Console.run(f"rm {' '.join(files)}")

  @staticmethod
  def call(executable, args):
    return Console.run(f"{executable} {' '.join(args)}")

  @staticmethod
  def rename(old, new):
    return Console.run(f"mv {old} {new}")

class NTCommander:
  @staticmethod
  def ls():
    return Console.run("dir")
    
  @staticmethod
  def clear():
    return Console.run("cls")

  @staticmethod
  def rm(files):
    return Console.run(f"del {' '.join(files)}")

  @staticmethod
  def call(executable, args):
    return Console.run(f"{executable} {' '.join(args)}")

  @staticmethod
  def rename(old, new):
    return Console.run(f"rename {old} {new}")

class Interface:
  def __init__(self):
    if os.name == "posix":
      self.commander = PosixCommander
    elif os.name == "nt":
      self.commander = NTCommander
  
  def ls(self):
    return self.commander.ls()
  
  def clear(self):
    return self.commander.clear()
  
  def rm(self, files):
    return self.commander.rm(files)
  
  def rename(self, old, new):
    return self.commander.rename(old, new)
  
  def call(self, executable, args):
    return self.commander.call(executable, args)

class CVBibliography:
  def __init__(self, config):
    self.name = config["name"]
    self.surname = config["surname"]
    self.abbrv = config["abbrv"]
    self.address = config["address"]
    #self.mobile = config["mobile"]
    self.email = config["email"]
    self.git = config["git"]
    self.linkedin = config["linkedin"]
    self.gender = config["gender"]
    self.nationality = config["nationality"]
    #self.birthday = config["birthday"]
  
  def compile(self, short: bool):
    return "\n".join([
      "\\bibliography{europasscv_example}",
      "\\ecvbibhighlight{" + self.surname + "}{" + self.name + "}{" + self.abbrv + "}",
      "\\ecvname{" + self.surname + " " + self.name + "}",
      "\\ecvaddress{" + self.address + "}",
      #"\\ecvmobile{" + self.mobile + "}",
      "\\ecvemail{" + self.email + "}",
      "\\ecvgithubpage{www.github.com/" + self.git + "}",
      "\\ecvgitlabpage{www.gitlab.com/" + self.git + "}",
      "\\ecvlinkedinpage{www.linkedin.com/in/" + self.linkedin + "}",
      "\\ecvgender{" + self.gender + "}",
      #"\\ecvdateofbirth{" + self.birthday + "}",
      "\\ecvnationality{" + self.nationality + "}"
    ])

class CVImport:
  def __init__(self, config):
    self.name = config["name"]
    self.codec = config["codec"]
  
  def compile(self, short: bool):
    return "\n".join([
      "% !TEX encoding = UTF-8",
      "% !TEX program = pdflatex",
      "% !TEX spellcheck = " + self.codec,
      "\\documentclass[" + self.name + ",a4paper]{europasscv}",
      "\\usepackage[" + self.name + "]{babel}",
      "\\usepackage[backend=biber,autolang=hyphen,sorting=none,style=numeric,maxbibnames=99,doi=false,isbn=false,maxcitenames=2]{biblatex}",
      "\\usepackage{csquotes}",
      "\\usepackage{europasscv-bibliography}"
    ])

class CVPersonalInfo:
  def __init__(self):
    pass
  
  def compile(self, short: bool):
    return "\\ecvpersonalinfo"

class CVPageBreak:
  def __init__(self):
    pass
  
  def compile(self, short: bool):
    return "\\pagebreak"

class CVWorkExperience:
  def __init__(self, config):
    self.start = config["start"]
    self.end = config["end"]
    self.title = config["title"]
    self.fields = config["fields"]
    self.urls = config["urls"]
    self.attachments = config["attachments"]
    self.minor = (config.get("minor") or False)
  
  def compile(self, short: bool):
    if short and self.minor:
      return ""
    return "\n".join([
      "\\ecvtitle{" + self.start + "--" + self.end + "}{" + self.title + "}"
    ] + [
      "\\ecvitem{}{" + field + "}" for field in self.fields
    ] + [
      "\\ecvitem{}{\\href{" + self.urls[url].replace("_", "\\_") + "}{Vai a " + url + ": " + self.urls[url].replace('_', '\\_') + "}}" for url in self.urls
    ] + [
      "\\ecvitem{}{" + f"Allegato: {attachment}" + "}" for attachment in self.attachments
    ] + [
      "\\ecvitem{}{\\includegraphics[width=12cm]{" + Curler.curlFile(self.attachments[attachment]).replace('_', '\\_') + "}}" for attachment in self.attachments
    ])

class CVEducationExperience:
  def __init__(self, config):
    self.start = config["start"]
    self.end = config["end"]
    self.title = config["title"]
    self.fields = config["fields"]
    self.urls = config["urls"]
    self.attachments = config["attachments"]
    self.minor = (config.get("minor") or False)
  
  def compile(self, short: bool):
    if short and self.minor:
      return ""
    return "\n".join([
      "\\ecvtitle{" + self.start + "--" + self.end + "}{" + self.title + "}"
    ] + [
      "\\ecvitem{}{" + field + "}" for field in self.fields
    ] + [
      "\\ecvitem{}{\\href{" + self.urls[url].replace("_", "\\_") + "}{Vai a " + url + ": " + self.urls[url].replace('_', '\\_') + "}}" for url in self.urls
    ] + [
      "\\ecvitem{}{" + f"Allegato: {attachment}" + "}" for attachment in self.attachments
    ] + [
      "\\ecvitem{}{\\includegraphics[width=12cm]{" + Curler.curlFile(self.attachments[attachment]).replace('_', '\\_') + "}}" for attachment in self.attachments
    ])

class CVPublication:
  def __init__(self, config):
    self.year = config["year"]
    self.title = config["title"]
    self.fields = config["fields"]
    self.urls = config["urls"]
    self.attachments = config["attachments"]
    self.minor = (config.get("minor") or False)
  
  def compile(self, short: bool):
    if short and self.minor:
      return ""
    return "\n".join([
      "\\ecvtitle{" + self.year + "}{" + self.title + "}"
    ] + [
      "\\ecvitem{}{" + field + "}" for field in self.fields
    ] + [
      "\\ecvitem{}{\\href{" + self.urls[url].replace("_", "\\_") + "}{Vai a " + url + ": " + self.urls[url].replace('_', '\\_') + "}}" for url in self.urls
    ] + [
      "\\ecvitem{}{" + f"Allegato: {attachment}" + "}" for attachment in self.attachments
    ] + [
      "\\ecvitem{}{\\includegraphics[width=12cm]{" + Curler.curlFile(self.attachments[attachment]).replace('_', '\\_') + "}}" for attachment in self.attachments
    ])

class CVDeliverable:
  def __init__(self, config):
    self.year = config["year"]
    self.title = config["title"]
    self.fields = config["fields"]
    self.urls = config["urls"]
    self.attachments = config["attachments"]
    self.minor = (config.get("minor") or False)
  
  def compile(self, short: bool):
    if short and self.minor:
      return ""
    return "\n".join([
      "\\ecvtitle{" + self.year + "}{" + self.title + "}"
    ] + [
      "\\ecvitem{}{" + field + "}" for field in self.fields
    ] + [
      "\\ecvitem{}{\\href{" + self.urls[url].replace("_", "\\_") + "}{Vai a " + url + ": " + self.urls[url].replace('_', '\\_') + "}}" for url in self.urls
    ] + [
      "\\ecvitem{}{" + f"Allegato: {attachment}" + "}" for attachment in self.attachments
    ] + [
      "\\ecvitem{}{\\includegraphics[width=12cm]{" + Curler.curlFile(self.attachments[attachment]).replace('_', '\\_') + "}}" for attachment in self.attachments
    ])

class CVLanguageSkill:
  def __init__(self, config):
    self.mothertongue = config["mothertongue"]
    self.langs = config["langs"]
  
  def compile(self, short: bool):
    text = ""
    
    text += "\n" + "\n".join([
      "\\ecvmothertongue{" + self.mothertongue + "}",
      "\\ecvlanguageheader"
    ])

    for lang in self.langs:
      text += "\n" + "\n".join([
        "\\ecvlanguage{" + lang["name"] + "}{" + "}{".join(lang["levels"]) + "}",
        "\\ecvlanguagecertificate{\\href{" + lang["certificate"]["url"] + "}{" + lang["certificate"]["issuer"] + "}}"
      ])
    
    text += "\n" + "\n".join([
      "\\ecvlanguagefooter"
    ])

    return text

class CVDigitalSkills:
  def __init__(self, config):
    self.levels = config["levels"]
  
  def compile(self, short: bool):
      return "\\ecvdigitalcompetence{" + "}{".join([ f"\\ecv{_}" for _ in self.levels]) + "}"

class CVTechSkills:
  def __init__(self, config):
    self.skills = config
  
  def compile(self, short: bool):
    text = ""

    text += "\\ecvblueitem{Competenze Tecniche}{"
    text += "\n" + "\\begin{ecvitemize}"

    for skill_name, skill_set in self.skills.items():
      text += "\n" + "\\item \\textbf{%s}: " % skill_name
      text += ", ".join(skill_set)

    text += "\n" + "\\end{ecvitemize}"
    text += "\n" + "}"

    return text

class CVPatentSkills:
  def __init__(self, config):
    self.title = config["title"]
    self.issuer = config["issuer"]
    self.start = config["start"]
    self.end = config["end"]
  
  def compile(self, short: bool):
    text = ""

    text += "\\ecvblueitem{" + self.title + "}{"
    text += "\n" + "\\begin{ecvitemize}"

    text += "\n" + "\\item Emittente: " + self.issuer
    text += "\n" + "\\item Rilasciato: " + self.start
    text += "\n" + "\\item Scadenza: " + self.end

    text += "\n" + "\\end{ecvitemize}"
    text += "\n" + "}"

    return text

class CVCertificationSkills:
  def __init__(self, config):
    self.title = config["title"]
    self.name = config["name"]
    self.number = config["number"]
    self.score = config["score"]
    self.minor = (config.get("minor") or False)
  
  def compile(self, short: bool):
    if short and self.minor:
      return ""
    text = ""

    text += "\\ecvblueitem{" + self.title + "}{"
    text += "\n" + "\\begin{ecvitemize}"

    text += "\n" + "\\item " + self.name
    text += "\n" + "\\item Numero Esame: " + self.number
    text += "\n" + "\\item Punteggio: " + self.score

    text += "\n" + "\\end{ecvitemize}"
    text += "\n" + "}"

    return text

class CVSkills:
  def __init__(self, config):
    self.skills = [
      CVLanguageSkill(config["language"]),
      CVDigitalSkills(config["digital"]),
      CVTechSkills(config["tech"])
    ] + [
      CVPatentSkills(cert) for cert in config["patents"]
    ] + [
      CVCertificationSkills(cert) for cert in config["certificates"]
    ]
  
  def compile(self, short: bool):
    text = "\\ecvsection{Competenze}"

    text += "\n" + "\n".join([_.compile(short) for _ in self.skills])
    
    return text

class CVWork:
  def __init__(self, config):
    self.experiences = [CVWorkExperience(_) for _ in config]
  
  def compile(self, short: bool):
    text = "\\ecvsection{Esperienze Lavorative}"
    text += "\n" + "\n".join([_.compile(short) for _ in self.experiences])
    return text

class CVEducation:
  def __init__(self, config):
    self.experiences = [CVEducationExperience(_) for _ in config]
  
  def compile(self, short: bool):
    text = "\\ecvsection{Istruzione e Formazione}"
    text += "\n" + "\n".join([_.compile(short) for _ in self.experiences])
    return text

class CVPublications:
  def __init__(self, config):
    self.experiences = [CVPublication(_) for _ in config]
  
  def compile(self, short: bool):
    text = "\\ecvsection{Pubblicazioni}"
    text += "\n" + "\n".join([_.compile(short) for _ in self.experiences])
    return text

class CVDeliverables:
  def __init__(self, config):
    self.experiences = [CVDeliverable(_) for _ in config]
  
  def compile(self, short: bool):
    text = "\\ecvsection{Manufatti}"
    text += "\n" + "\n".join([_.compile(short) for _ in self.experiences])
    return text

class CVDream:
  def __init__(self, config):
    self.text = config["text"]
    self.minor = (config.get("minor") or False)

  def compile(self, short: bool):
    if short and self.minor:
      return ""
    return "\n".join([
      "\\ecvsection{Aspirazioni Professionali}",
      "\\ecvitem{}{" + self.text + "}"
    ])

class CVPrivacy:
  def __init__(self):
    pass

  def compile(self, short: bool):
    return "\n".join([
      "\\ecvsection{Privacy}",
      "\\ecvitem{}{Autorizzo il trattamento dei miei dati personali presenti nel CV ai sensi dell’art. 13 d. lgs. 30 giugno 2003 n. 196 - \"Codice in materia di protezione dei dati personali\" e dell’art. 13 GDPR 679/16 - \"Regolamento europeo sulla protezione dei dati persona\"}"
    ])

class CVCopyright:
  def __init__(self):
    pass

  def compile(self, short: bool):
    return "\n".join([
      "\\ecvsection{Copyright}",
      "\\ecvitem{}{Questo documento \\`e stato generato automaticamente con il software \\textit{eurogen} sviluppato da Refolli Francesco (\\href{https://github.com/windflaag/eurogen}{github.com/windflaag/eurogen}), rilasciato con licenza \\href{https://www.gnu.org/licenses/gpl-3.0.html}{GNU GPL v3}.}"
    ])

class CVDocument:
  def __init__(self, config):
    self.preamble = [
      CVImport(config["language"]),
      CVBibliography(config["bibliography"])
    ]

    self.page = [
      CVPersonalInfo(),
      CVWork(config["work"]),
      CVPublications(config["publications"]),
      CVDeliverables(config["deliverables"]),
      CVEducation(config["education"]),
      #CVPageBreak(),
      CVSkills(config["skills"]),
      CVDream(config["dream"]),
      CVPrivacy(),
      CVCopyright()
    ]
  
  def compile(self, short: bool):
    text = "\n".join([_.compile(short) for _ in self.preamble])

    text += "\n" + "\n".join([
      "\\begin{document}",
      "\\begin{europasscv}"
    ])

    text += "\n" + "\n".join([_.compile(short) for _ in self.page])

    text += "\n" + "\n".join([
      "\\end{europasscv}",
      "\\end{document}"
    ])

    return text

class Curriculum:
  def __init__(self, output = "cv.pdf"):
    self.interface = Interface()
    self.output = output
    self.info = []
    
  def compile(self, short: bool):
    file = open("cv.tex", "w")

    text = ""

    for info in self.info:
      text += f"\n{info.compile(short)}\n"
    
    file.write(text)
    file.close()
  
  def addInfo(self, info):
    self.info.append(info)
  
  def build(self):
    if not os.path.exists("./build"):
      self.interface.call("mkdir", ["build"])
    
    self.interface.call("pdflatex", ["-output-directory=./build", "cv.tex"])
    self.interface.rename("build/cv.pdf", self.output)

if __name__ == "__main__":
  argument_parser = argparse.ArgumentParser(description="Europass CV Generator")
  argument_parser.add_argument("-s", "--short", action="store_true", default=False, help="Generates a SHORT version of the CV (e.g. hides all 'minor' marked infos)")
  command_line_arguments = argument_parser.parse_args(sys.argv[1:])

  cv = Curriculum()

  with open("cv.json", "r") as file:
    jsonText = file.read()
    file.close()

    config = json.loads(jsonText)
    cv.addInfo(CVDocument(config))

  cv.compile(short=command_line_arguments.short)
  cv.build()
