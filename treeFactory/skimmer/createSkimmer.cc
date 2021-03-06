/*
Copyright 2015 Sébastien Brochet

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
*/

#include <Python.h>

#include <treeFactory/config.h>

#include <iostream>
#include <fstream>
#include <memory>
#include <cstdio>

#include <TChain.h>
#include <TApplication.h>

// Ugly hack to access list of leaves in the formula
#define protected public
#include <TTreeFormula.h>
#undef protected

#include <uuid/uuid.h>

#include <tclap/CmdLine.h>

#include <ctemplate/template.h>

struct InputBranch {
    std::string name;
    std::string type;
};

struct OutputBranch {
    std::string name;
    std::string unique_name;
    std::string variable;

};

struct Tree {
    std::string name;
    std::string cut;
    std::vector<OutputBranch> branches;
};

#define CHECK_AND_GET(var, obj) if (PyDict_Contains(value, obj) == 1) { \
    PyObject* item = PyDict_GetItem(value, obj); \
    if (! PyString_Check(item)) {\
        std::cerr << "Error: the '" << PyString_AsString(obj) << "' value must be a string" << std::endl; \
        return false; \
    } \
    var = PyString_AsString(item); \
} else { \
    std::cerr << "Error: '" << PyString_AsString(obj) << "' key is missing" << std::endl; \
    return false; \
}

#define GET(var, obj) if (PyDict_Contains(value, obj) == 1) { \
    PyObject* item = PyDict_GetItem(value, obj); \
    if (! PyString_Check(item)) {\
        std::cerr << "Error: the '" << PyString_AsString(obj) << "' value must be a string" << std::endl; \
        return false; \
    } \
    var = PyString_AsString(item); \
}

bool output_branch_from_PyObject(PyObject* value, OutputBranch& branch) {
    static PyObject* PY_NAME = PyString_FromString("name");
    static PyObject* PY_VARIABLE = PyString_FromString("variable");

    if (! PyDict_Check(value)) {
        std::cerr << "Error: branches dictionnary value must be a dictionnary" << std::endl;
    }

    CHECK_AND_GET(branch.name, PY_NAME);
    CHECK_AND_GET(branch.variable, PY_VARIABLE);

    return true;
}

std::string get_uuid();

bool tree_from_PyObject(PyObject* value, Tree& tree) {
    static PyObject* PY_NAME = PyString_FromString("name");
    static PyObject* PY_CUT = PyString_FromString("cut");
    static PyObject* PY_BRANCHES = PyString_FromString("branches");

    CHECK_AND_GET(tree.name, PY_NAME);

    tree.cut = "1";
    GET(tree.cut, PY_CUT);
    
    if (PyDict_Contains(value, PY_BRANCHES) == 0) {
        std::cout << "No branches declared in tree" << std::endl;
        return false;
    }

    PyObject* py_branches = PyDict_GetItem(value, PY_BRANCHES);
    
    if (! PyList_Check(py_branches)) {
        std::cerr << "The '" << PyString_AsString(PY_BRANCHES) << "' value is not a list" << std::endl;
        return false;
    }

    size_t l = PyList_Size(py_branches);
    if (! l)
        return false;

    for (size_t i = 0; i < l; i++) {
        PyObject* item = PyList_GetItem(py_branches, i);

        OutputBranch branch;
        if (output_branch_from_PyObject(item, branch)) {
            branch.unique_name = get_uuid();
            tree.branches.push_back(branch);
        }
    }

    return true;    
}

std::string get_uuid() {
    uuid_t out;
    uuid_generate(out);

    std::string uuid;
    uuid.resize(37);

    uuid_unparse(out, &uuid[0]);

    uuid[8] = '_';
    uuid[13] = '_';
    uuid[18] = '_';
    uuid[23] = '_';

    // Remove null terminator
    uuid.resize(36);

    // Ensure name starts with a letter to be a valid C++ identifier
    uuid = "p_" + uuid;

    return uuid;
}

inline TBranch* getTopBranch(TBranch* branch) {
    if (! branch)
        return nullptr;

    if (branch == branch->GetMother())
        return branch;

    return getTopBranch(branch->GetMother());
}

inline std::string getTemplate(const std::string& name) {
    std::string p = TEMPLATE_PATH;
    p += "/" + name + ".tpl";

    return p;
}

std::vector<std::string> split(const std::string& s, const std::string& delimiters) {

    std::vector<std::string> result;

    size_t current;
    size_t next = -1;
    do
    {
        next = s.find_first_not_of(delimiters, next + 1);
        if (next == std::string::npos)
            break;
        next -= 1;

        current = next + 1;
        next = s.find_first_of(delimiters, current);
        result.push_back(s.substr(current, next - current));
    }
    while (next != std::string::npos);

    return result;
}

bool execute(const std::string& skeleton, const std::string& config_file, std::string output_dir = "");

/**
 * Parse a python file and extract the list of branches to create
 */
bool get_output_tree(const std::string& python_file, Tree& tree) {

    std::FILE* f = std::fopen(python_file.c_str(), "r");
    if (!f) {
        std::cerr << "Failed to open '" << python_file << "'" <<std::endl;
        return false;
    }

    const std::string TREE_KEY_NAME = "tree";

    // Get a reference to the main module
    // and global dictionary
    PyObject* main_module = PyImport_AddModule("__main__");
    PyObject* global_dict = PyModule_GetDict(main_module);

    // If PyROOT is used inside the script, it performs some cleanups when the python env. is destroyed. This cleanup makes ROOT unusable afterwards.
    // The cleanup function is registered with the `atexit` module.
    // The solution is to not execute the cleanup function. For that, before destroying the python env, we check the list of exit functions,
    // and delete the one from PyROOT if found

    // Ensure the module is loaded
    PyObject* atexit_module = PyImport_ImportModule("atexit");

    // Execute the script
    PyObject* script_result = PyRun_File(f, python_file.c_str(), Py_file_input, global_dict, global_dict);

    if (! script_result) {
        PyErr_Print();
        return false;
    } else {
        PyObject* py_tree = PyDict_GetItemString(global_dict, TREE_KEY_NAME.c_str());
        if (!py_tree) {
            std::cerr << "No '" << TREE_KEY_NAME << "' variable declared in python script" << std::endl;
            return false;
        }

        if (! PyDict_Check(py_tree)) {
            std::cerr << "The '" << TREE_KEY_NAME << "' variable is not a dictionary" << std::endl;
            return false;
        }

        if (! tree_from_PyObject(py_tree, tree))
            return false;
    }

    PyObject* atexit_exithandlers = PyObject_GetAttrString(atexit_module, "_exithandlers");
    for (size_t i = 0; i < PySequence_Size(atexit_exithandlers); i++) {
        PyObject* tuple = PySequence_GetItem(atexit_exithandlers, i);
        PyObject* f = PySequence_GetItem(tuple, 0);
        PyObject* module = PyFunction_GetModule(f);

        if (module && strcmp(PyString_AsString(module), "ROOT") == 0) {
            PySequence_DelItem(atexit_exithandlers, i);
            break;
        }
    }

    return true;
}

bool execute(const std::string& skeleton, const std::string& config_file, std::string output_dir/* = ""*/) {

    Tree output_tree;
    // If an output directory is specified, use it, otherwise use the current directory
    if (output_dir == "")
      output_dir = ".";

    std::map<std::string, std::string> unique_names;

    if (! get_output_tree(config_file, output_tree))
        return false;

    std::cout << "List of branches in the output tree: ";
    for (size_t i = 0; i < output_tree.branches.size(); i++) {
        std::cout << "'" << output_tree.branches[i].name << "'";
        if (i != output_tree.branches.size() - 1)
            std::cout << ", ";
    }
    std::cout << std::endl;

    std::unique_ptr<TChain> t(new TChain("t"));
    t->Add(skeleton.c_str());

    std::vector<InputBranch> branches;
    std::function<void(TTreeFormula*)> getBranches = [&branches, &getBranches](TTreeFormula* f) {
        if (!f)
            return;

        for (size_t i = 0; i < f->GetNcodes(); i++) {
            TLeaf* leaf = f->GetLeaf(i);
            if (! leaf)
                continue;

            TBranch* p_branch = getTopBranch(leaf->GetBranch());

            InputBranch branch;
            branch.name = p_branch->GetName();
            if (std::find_if(branches.begin(), branches.end(), [&branch](const InputBranch& b) {  return b.name == branch.name;  }) == branches.end()) {
                branch.type = p_branch->GetClassName();
                if (branch.type.empty())
                    branch.type = leaf->GetTypeName();

                branches.push_back(branch);
            }

            for (size_t j = 0; j < f->fNdimensions[i]; j++) {
                if (f->fVarIndexes[i][j])
                    getBranches(f->fVarIndexes[i][j]);
            }
        }

        for (size_t i = 0; i < f->fAliases.GetEntriesFast(); i++) {
            getBranches((TTreeFormula*) f->fAliases.UncheckedAt(i));
        }
    };

    // Tree cut
    std::shared_ptr<TTreeFormula> cut_formula(new TTreeFormula("selector", output_tree.cut.c_str(), t.get()));
    getBranches(cut_formula.get());

    std::string output_branches_declaration;
    std::string output_branches_filling;
    for (auto& b: output_tree.branches) {
        // Create formulas
        std::shared_ptr<TTreeFormula> variable_formula(new TTreeFormula("variable", b.variable.c_str(), t.get()));

        getBranches(variable_formula.get());

        //hists_declaration += "    std::unique_ptr<" + histogram_type + "> " + p.name + "(new " + histogram_type + "(\"" + p.name + "\", \"" + title + "\", " + binning + ")); " + p.name + "->SetDirectory(nullptr);\n";
        output_branches_declaration += "    float& " + b.unique_name + " = output_tree[\"" + b.name + "\"].write<float>();\n";

        output_branches_filling += "        " + b.unique_name + " = (" + b.variable + ");\n";
    }

    // Sort alphabetically
    std::sort(branches.begin(), branches.end(), [](const InputBranch& a, const InputBranch& b) {
            return a.name < b.name;
            });

    std::string input_branches_declaration;
    for (const auto& branch: branches)  {
        input_branches_declaration += "const " + branch.type + "& " + branch.name + " = tree[\"" + branch.name + "\"].read<" + branch.type + ">();\n        ";
    }

    ctemplate::TemplateDictionary header("header");
    header.SetValue("BRANCHES", input_branches_declaration);

    std::string output;
    ctemplate::ExpandTemplate(getTemplate("Skimmer.h"), ctemplate::DO_NOT_STRIP, &header, &output);

    std::ofstream out(output_dir + "/Skimmer.h");
    out << output;
    out.close();

    output.clear();

    // Create cut string
    std::string global_cut = "        if (! (" + output_tree.cut + ")) { continue; }";

    ctemplate::TemplateDictionary source("source");
    source.SetValue("OUTPUT_TREE_NAME", output_tree.name);
    source.SetValue("OUTPUT_BRANCHES_DECLARATION", output_branches_declaration);
    source.SetValue("GLOBAL_CUT", global_cut);
    source.SetValue("OUTPUT_BRANCHES_FILLING", output_branches_filling);
    ctemplate::ExpandTemplate(getTemplate("Skimmer.cc"), ctemplate::DO_NOT_STRIP, &source, &output);

    out.open(output_dir + "/Skimmer.cc");
    out << output;
    out.close();

    return true;
}

int main( int argc, char* argv[]) {

    try {

        TCLAP::CmdLine cmd("Create histograms from trees", ' ', "0.2.0");

        TCLAP::ValueArg<std::string> skeletonArg("i", "input", "Input file containing a skeleton tree", true, "", "ROOT file", cmd);
        TCLAP::ValueArg<std::string> outputArg("o", "output", "Output directory", false, "", "FOLDER", cmd);
        TCLAP::UnlabeledValueArg<std::string> treeArg("tree", "A python script which will be executed and should describe the tree to create", true, "", "Python script", cmd);

        cmd.parse(argc, argv);

        /*
         * When PyROOT is loaded, it creates it's own ROOT application ([1] and [2]). We do not want this to happen,
         * because it messes with our already loaded ROOT.
         *
         * To prevent this, we create here our own application (which does nothing), just to prevent `CreatePyROOTApplication`
         * to do anything.
         *
         * [1] https://github.com/root-mirror/root/blob/0a62e34aa86b812651cfcf9526ba03b975adaa5c/bindings/pyroot/ROOT.py#L476
         * [2] https://github.com/root-mirror/root/blob/0a62e34aa86b812651cfcf9526ba03b975adaa5c/bindings/pyroot/src/TPyROOTApplication.cxx#L117
         */

        std::unique_ptr<TApplication> app(new TApplication("dummy", 0, NULL));

        Py_Initialize();

        bool ret = execute(skeletonArg.getValue(), treeArg.getValue(), outputArg.getValue());

        Py_Finalize();

        return (ret ? 0 : 1);

    } catch (TCLAP::ArgException &e) {
        std::cerr << "error: " << e.error() << " for arg " << e.argId() << std::endl;
        return 1;
    }

    return 0;
}

