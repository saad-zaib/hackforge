// ConfigManager.jsx - UPDATED FOR NEW CONFIG FORMAT
// Enhanced with full database schema support and infrastructure configuration

import React, { useState, useEffect } from 'react';
import {
  Settings, Plus, RefreshCw, Trash2, Loader,
  CheckCircle, AlertCircle, FileCode, Hammer,
  ChevronRight, X, Sparkles, Code, Zap, Rocket,
  ChevronDown, ChevronUp, Database, Box, Upload
} from 'lucide-react';
import api from '../services/api';

const ConfigManager = () => {
  const [configs, setConfigs] = useState([]);
  const [showCreateForm, setShowCreateForm] = useState(false);
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState(null);
  const [generatingMachine, setGeneratingMachine] = useState(null);
  const [expandedSections, setExpandedSections] = useState({
    basic: true,
    infrastructure: false,
    database: false,
    variants: false,
    entryPoints: false,
    mutation: false,
    aiHints: false
  });

  // Updated Config State - NEW FORMAT
  const [newConfig, setNewConfig] = useState({
    vulnerability_id: '',
    name: '',
    category: '',
    difficulty_range: [1, 5],
    description: '',

    // Infrastructure
    infrastructure: {
      needs_database: false,
      database_type: 'mysql',
      needs_file_system: false,
      needs_external_service: false,
      docker_requirements: {
        base_image: 'php:8.0-apache',
        extensions: ['mysqli', 'pdo', 'pdo_mysql'],
        packages: ['curl', 'vim', 'net-tools'],
        ports: [80]
      }
    },

    // Database Schema (only if needs_database is true)
    database_schema: {
      tables: [],
      seed_data: {},
      flag_location: 'users.secret_data WHERE username=\'admin\''
    },

    // Variants with enhanced structure
    variants: [{
      name: '',
      description: '',
      difficulty: 2,
      exploit_example: '',
      sink_function: '',
      output_type: ''
    }],

    // Entry Points with enhanced structure
    entry_points: [{
      type: '',
      parameter_name: '',
      context: ''
    }],

    // Mutation Axes with structured filters
    mutation_axes: {
      filters: {
        basic: [],
        medium: [],
        advanced: []
      },
      contexts: [],
      sinks: []
    },

    // AI Generation Hints
    ai_generation_hints: {
      code_structure: '',
      database_connection: '',
      vulnerability_placement: '',
      output_format: '',
      dockerfile_notes: ''
    },

    // Exploit Examples
    exploit_examples: []
  });

  useEffect(() => {
    loadConfigs();
  }, []);

  const loadConfigs = async () => {
    try {
      setLoading(true);
      const data = await api.getConfigs();
      setConfigs(data);
    } catch (error) {
      showMessage('Failed to load configs: ' + error.message, 'error');
    } finally {
      setLoading(false);
    }
  };

  const showMessage = (text, type = 'info') => {
    setMessage({ text, type });
    setTimeout(() => setMessage(null), 8000);
  };

  const toggleSection = (section) => {
    setExpandedSections(prev => ({
      ...prev,
      [section]: !prev[section]
    }));
  };

  const handleCreateConfig = async (e, autoGenerate = true) => {
    e.preventDefault();

    try {
      setLoading(true);

      // Clean up config before sending
      const cleanConfig = {
        ...newConfig,
        variants: newConfig.variants.filter(v => v.name.trim()),
        entry_points: newConfig.entry_points.filter(ep => ep.type.trim()),
        mutation_axes: {
          filters: {
            basic: newConfig.mutation_axes.filters.basic.filter(f => f.name?.trim()),
            medium: newConfig.mutation_axes.filters.medium.filter(f => f.name?.trim()),
            advanced: newConfig.mutation_axes.filters.advanced.filter(f => f.name?.trim())
          },
          contexts: newConfig.mutation_axes.contexts.filter(c => c.name?.trim()),
          sinks: newConfig.mutation_axes.sinks.filter(s => s.trim())
        },
        exploit_examples: newConfig.exploit_examples.filter(ex => ex.payload?.trim())
      };

      // Remove database_schema if database not needed
      if (!cleanConfig.infrastructure.needs_database) {
        delete cleanConfig.database_schema;
      }

      // Add auto_generate query parameter
      const result = await api.createConfigWithMachine(cleanConfig, autoGenerate);

      if (result.auto_generated && result.machine) {
        showMessage(
          `🎉 Config + Machine ready! ${result.machine.machine_id} at ${result.machine.url || 'Building...'}`,
          'success'
        );
      } else {
        showMessage('✓ Config created successfully!', 'success');
      }

      setShowCreateForm(false);
      loadConfigs();
      resetForm();

    } catch (error) {
      showMessage('Failed to create config: ' + error.message, 'error');
    } finally {
      setLoading(false);
    }
  };

  const resetForm = () => {
    setNewConfig({
      vulnerability_id: '',
      name: '',
      category: '',
      difficulty_range: [1, 5],
      description: '',
      infrastructure: {
        needs_database: false,
        database_type: 'mysql',
        needs_file_system: false,
        needs_external_service: false,
        docker_requirements: {
          base_image: 'php:8.0-apache',
          extensions: ['mysqli', 'pdo', 'pdo_mysql'],
          packages: ['curl', 'vim', 'net-tools'],
          ports: [80]
        }
      },
      database_schema: {
        tables: [],
        seed_data: {},
        flag_location: 'users.secret_data WHERE username=\'admin\''
      },
      variants: [{ name: '', description: '', difficulty: 2, exploit_example: '', sink_function: '', output_type: '' }],
      entry_points: [{ type: '', parameter_name: '', context: '' }],
      mutation_axes: {
        filters: { basic: [], medium: [], advanced: [] },
        contexts: [],
        sinks: []
      },
      ai_generation_hints: {
        code_structure: '',
        database_connection: '',
        vulnerability_placement: '',
        output_format: '',
        dockerfile_notes: ''
      },
      exploit_examples: []
    });
  };

  const handleGenerateMachine = async (category) => {
    try {
      setGeneratingMachine(category);
      showMessage(`🚀 Generating machine from ${category}...`, 'info');

      const result = await api.generateMachineFromConfig(category);

      showMessage(
        `🎉 Machine ready! ${result.machine_id} at ${result.url || 'http://4.231.90.52:8080'}`,
        'success'
      );

      setTimeout(() => loadConfigs(), 2000);

    } catch (error) {
      showMessage('Failed to generate machine: ' + error.message, 'error');
    } finally {
      setGeneratingMachine(null);
    }
  };

  // Variant helpers
  const addVariant = () => {
    setNewConfig(prev => ({
      ...prev,
      variants: [...prev.variants, {
        name: '',
        description: '',
        difficulty: 2,
        exploit_example: '',
        sink_function: '',
        output_type: ''
      }]
    }));
  };

  const updateVariant = (index, field, value) => {
    setNewConfig(prev => {
      const newVariants = [...prev.variants];
      newVariants[index] = { ...newVariants[index], [field]: value };
      return { ...prev, variants: newVariants };
    });
  };

  const removeVariant = (index) => {
    setNewConfig(prev => ({
      ...prev,
      variants: prev.variants.filter((_, i) => i !== index)
    }));
  };

  // Entry point helpers
  const addEntryPoint = () => {
    setNewConfig(prev => ({
      ...prev,
      entry_points: [...prev.entry_points, { type: '', parameter_name: '', context: '' }]
    }));
  };

  const updateEntryPoint = (index, field, value) => {
    setNewConfig(prev => {
      const newEPs = [...prev.entry_points];
      newEPs[index] = { ...newEPs[index], [field]: value };
      return { ...prev, entry_points: newEPs };
    });
  };

  const removeEntryPoint = (index) => {
    setNewConfig(prev => ({
      ...prev,
      entry_points: prev.entry_points.filter((_, i) => i !== index)
    }));
  };

  // Database table helpers
  const addTable = () => {
    setNewConfig(prev => ({
      ...prev,
      database_schema: {
        ...prev.database_schema,
        tables: [...prev.database_schema.tables, { name: '', columns: ['id INT PRIMARY KEY AUTO_INCREMENT'] }]
      }
    }));
  };

  const updateTable = (index, field, value) => {
    setNewConfig(prev => {
      const newTables = [...prev.database_schema.tables];
      newTables[index] = { ...newTables[index], [field]: value };
      return {
        ...prev,
        database_schema: { ...prev.database_schema, tables: newTables }
      };
    });
  };

  const removeTable = (index) => {
    setNewConfig(prev => ({
      ...prev,
      database_schema: {
        ...prev.database_schema,
        tables: prev.database_schema.tables.filter((_, i) => i !== index)
      }
    }));
  };

  const addTableColumn = (tableIndex) => {
    setNewConfig(prev => {
      const newTables = [...prev.database_schema.tables];
      newTables[tableIndex].columns = [...newTables[tableIndex].columns, ''];
      return {
        ...prev,
        database_schema: { ...prev.database_schema, tables: newTables }
      };
    });
  };

  const updateTableColumn = (tableIndex, colIndex, value) => {
    setNewConfig(prev => {
      const newTables = [...prev.database_schema.tables];
      newTables[tableIndex].columns[colIndex] = value;
      return {
        ...prev,
        database_schema: { ...prev.database_schema, tables: newTables }
      };
    });
  };

  const removeTableColumn = (tableIndex, colIndex) => {
    setNewConfig(prev => {
      const newTables = [...prev.database_schema.tables];
      newTables[tableIndex].columns = newTables[tableIndex].columns.filter((_, i) => i !== colIndex);
      return {
        ...prev,
        database_schema: { ...prev.database_schema, tables: newTables }
      };
    });
  };

  // Context helpers
  const addContext = () => {
    setNewConfig(prev => ({
      ...prev,
      mutation_axes: {
        ...prev.mutation_axes,
        contexts: [...prev.mutation_axes.contexts, {
          name: '',
          query_template: '',
          ui_theme: '',
          description: ''
        }]
      }
    }));
  };

  const updateContext = (index, field, value) => {
    setNewConfig(prev => {
      const newContexts = [...prev.mutation_axes.contexts];
      newContexts[index] = { ...newContexts[index], [field]: value };
      return {
        ...prev,
        mutation_axes: { ...prev.mutation_axes, contexts: newContexts }
      };
    });
  };

  const removeContext = (index) => {
    setNewConfig(prev => ({
      ...prev,
      mutation_axes: {
        ...prev.mutation_axes,
        contexts: prev.mutation_axes.contexts.filter((_, i) => i !== index)
      }
    }));
  };

  // Filter helpers
  const addFilter = (level) => {
    setNewConfig(prev => ({
      ...prev,
      mutation_axes: {
        ...prev.mutation_axes,
        filters: {
          ...prev.mutation_axes.filters,
          [level]: [...prev.mutation_axes.filters[level], {
            name: '',
            type: '',
            php_code: '',
            description: '',
            bypassable: true,
            bypass_hint: ''
          }]
        }
      }
    }));
  };

  const updateFilter = (level, index, field, value) => {
    setNewConfig(prev => {
      const newFilters = [...prev.mutation_axes.filters[level]];
      newFilters[index] = { ...newFilters[index], [field]: value };
      return {
        ...prev,
        mutation_axes: {
          ...prev.mutation_axes,
          filters: {
            ...prev.mutation_axes.filters,
            [level]: newFilters
          }
        }
      };
    });
  };

  const removeFilter = (level, index) => {
    setNewConfig(prev => ({
      ...prev,
      mutation_axes: {
        ...prev.mutation_axes,
        filters: {
          ...prev.mutation_axes.filters,
          [level]: prev.mutation_axes.filters[level].filter((_, i) => i !== index)
        }
      }
    }));
  };

  // Sink helpers
  const addSink = () => {
    setNewConfig(prev => ({
      ...prev,
      mutation_axes: {
        ...prev.mutation_axes,
        sinks: [...prev.mutation_axes.sinks, '']
      }
    }));
  };

  const updateSink = (index, value) => {
    setNewConfig(prev => {
      const newSinks = [...prev.mutation_axes.sinks];
      newSinks[index] = value;
      return {
        ...prev,
        mutation_axes: { ...prev.mutation_axes, sinks: newSinks }
      };
    });
  };

  const removeSink = (index) => {
    setNewConfig(prev => ({
      ...prev,
      mutation_axes: {
        ...prev.mutation_axes,
        sinks: prev.mutation_axes.sinks.filter((_, i) => i !== index)
      }
    }));
  };

  // Exploit example helpers
  const addExploitExample = () => {
    setNewConfig(prev => ({
      ...prev,
      exploit_examples: [...prev.exploit_examples, {
        payload: '',
        description: '',
        expected_result: ''
      }]
    }));
  };

  const updateExploitExample = (index, field, value) => {
    setNewConfig(prev => {
      const newExamples = [...prev.exploit_examples];
      newExamples[index] = { ...newExamples[index], [field]: value };
      return { ...prev, exploit_examples: newExamples };
    });
  };

  const removeExploitExample = (index) => {
    setNewConfig(prev => ({
      ...prev,
      exploit_examples: prev.exploit_examples.filter((_, i) => i !== index)
    }));
  };

  if (loading && configs.length === 0) {
    return (
      <div className="min-h-screen bg-black flex items-center justify-center">
        <div className="text-center">
          <Loader className="w-12 h-12 text-orange-500 animate-spin mx-auto mb-4" />
          <p className="text-gray-400">Loading configs...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-black text-white">
      <div className="max-w-7xl mx-auto px-6 py-8">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-4xl font-bold mb-2 bg-gradient-to-r from-white via-orange-500 to-orange-600 bg-clip-text text-transparent">
            Vulnerability Configs
          </h1>
          <p className="text-gray-400">Enhanced format with database and infrastructure support</p>
        </div>

        {/* Message Toast */}
        {message && (
          <div
            className={`mb-6 p-4 rounded-2xl border flex items-center gap-3 ${
              message.type === 'error'
                ? 'bg-red-950/20 border-red-500/50'
                : message.type === 'success'
                ? 'bg-green-950/20 border-green-500/50'
                : 'bg-blue-950/20 border-blue-500/50'
            }`}
          >
            {message.type === 'error' ? (
              <AlertCircle className="w-5 h-5 text-red-500" />
            ) : message.type === 'success' ? (
              <CheckCircle className="w-5 h-5 text-green-500" />
            ) : (
              <Loader className="w-5 h-5 text-blue-500 animate-spin" />
            )}
            <span className={
              message.type === 'error' ? 'text-red-400' :
              message.type === 'success' ? 'text-green-400' : 'text-blue-400'
            }>{message.text}</span>
          </div>
        )}

        {/* Action Buttons */}
        <div className="mb-8 flex flex-wrap gap-4">
          <button
            onClick={() => setShowCreateForm(!showCreateForm)}
            className="px-6 py-3 bg-orange-500 hover:bg-orange-600 text-white rounded-xl transition-all duration-300 flex items-center gap-2 hover:scale-105 active:scale-95"
          >
            {showCreateForm ? <X className="w-5 h-5" /> : <Plus className="w-5 h-5" />}
            {showCreateForm ? 'Cancel' : 'Create Config'}
          </button>

          <button
            onClick={loadConfigs}
            disabled={loading}
            className="px-6 py-3 bg-gray-800 hover:bg-gray-700 text-white rounded-xl transition-all duration-300 flex items-center gap-2 hover:scale-105 active:scale-95"
          >
            <RefreshCw className={`w-5 h-5 ${loading ? 'animate-spin' : ''}`} />
            Refresh
          </button>
        </div>

        {/* CREATE FORM */}
        {showCreateForm && (
          <div className="mb-8 rounded-2xl border border-gray-900 bg-gradient-to-br from-gray-900/50 to-black/50 backdrop-blur p-6">
            <h2 className="text-2xl font-bold mb-6 flex items-center gap-2">
              <FileCode className="w-6 h-6 text-orange-500" />
              Create Vulnerability Config
            </h2>

            <form onSubmit={(e) => handleCreateConfig(e, true)} className="space-y-6">

              {/* BASIC INFO */}
              <div className="border border-gray-800 rounded-xl p-6 bg-black/30">
                <button
                  type="button"
                  onClick={() => toggleSection('basic')}
                  className="w-full flex items-center justify-between mb-4"
                >
                  <h3 className="text-xl font-bold flex items-center gap-2">
                    <Code className="w-5 h-5 text-orange-500" />
                    Basic Information
                  </h3>
                  {expandedSections.basic ? <ChevronUp /> : <ChevronDown />}
                </button>

                {expandedSections.basic && (
                  <div className="space-y-4">
                    <div className="grid grid-cols-2 gap-4">
                      <input
                        type="text"
                        required
                        placeholder="Vulnerability ID (e.g., sqli_001)"
                        value={newConfig.vulnerability_id}
                        onChange={(e) => setNewConfig({...newConfig, vulnerability_id: e.target.value})}
                        className="px-4 py-3 bg-black/50 border border-gray-800 rounded-xl text-white focus:outline-none focus:border-orange-500"
                      />
                      <input
                        type="text"
                        required
                        placeholder="Name (e.g., SQL Injection)"
                        value={newConfig.name}
                        onChange={(e) => setNewConfig({...newConfig, name: e.target.value})}
                        className="px-4 py-3 bg-black/50 border border-gray-800 rounded-xl text-white focus:outline-none focus:border-orange-500"
                      />
                    </div>
                    <input
                      type="text"
                      required
                      placeholder="Category (e.g., sql_injection)"
                      value={newConfig.category}
                      onChange={(e) => setNewConfig({...newConfig, category: e.target.value})}
                      className="w-full px-4 py-3 bg-black/50 border border-gray-800 rounded-xl text-white focus:outline-none focus:border-orange-500"
                    />
                    <textarea
                      required
                      rows="3"
                      placeholder="Description..."
                      value={newConfig.description}
                      onChange={(e) => setNewConfig({...newConfig, description: e.target.value})}
                      className="w-full px-4 py-3 bg-black/50 border border-gray-800 rounded-xl text-white focus:outline-none focus:border-orange-500"
                    />
                    <div className="grid grid-cols-2 gap-4">
                      <div>
                        <label className="block text-sm text-gray-400 mb-2">Min Difficulty</label>
                        <input
                          type="number"
                          min="1"
                          max="5"
                          value={newConfig.difficulty_range[0]}
                          onChange={(e) => setNewConfig({
                            ...newConfig,
                            difficulty_range: [parseInt(e.target.value), newConfig.difficulty_range[1]]
                          })}
                          className="w-full px-4 py-3 bg-black/50 border border-gray-800 rounded-xl text-white focus:outline-none focus:border-orange-500"
                        />
                      </div>
                      <div>
                        <label className="block text-sm text-gray-400 mb-2">Max Difficulty</label>
                        <input
                          type="number"
                          min="1"
                          max="5"
                          value={newConfig.difficulty_range[1]}
                          onChange={(e) => setNewConfig({
                            ...newConfig,
                            difficulty_range: [newConfig.difficulty_range[0], parseInt(e.target.value)]
                          })}
                          className="w-full px-4 py-3 bg-black/50 border border-gray-800 rounded-xl text-white focus:outline-none focus:border-orange-500"
                        />
                      </div>
                    </div>
                  </div>
                )}
              </div>

              {/* INFRASTRUCTURE */}
              <div className="border border-gray-800 rounded-xl p-6 bg-black/30">
                <button
                  type="button"
                  onClick={() => toggleSection('infrastructure')}
                  className="w-full flex items-center justify-between mb-4"
                >
                  <h3 className="text-xl font-bold flex items-center gap-2">
                    <Box className="w-5 h-5 text-orange-500" />
                    Infrastructure Requirements
                  </h3>
                  {expandedSections.infrastructure ? <ChevronUp /> : <ChevronDown />}
                </button>

                {expandedSections.infrastructure && (
                  <div className="space-y-4">
                    <div className="grid grid-cols-2 gap-4">
                      <label className="flex items-center gap-2 text-sm">
                        <input
                          type="checkbox"
                          checked={newConfig.infrastructure.needs_database}
                          onChange={(e) => setNewConfig({
                            ...newConfig,
                            infrastructure: { ...newConfig.infrastructure, needs_database: e.target.checked }
                          })}
                          className="w-4 h-4 rounded bg-black border-gray-700"
                        />
                        <Database className="w-4 h-4" />
                        Needs Database
                      </label>

                      <label className="flex items-center gap-2 text-sm">
                        <input
                          type="checkbox"
                          checked={newConfig.infrastructure.needs_file_system}
                          onChange={(e) => setNewConfig({
                            ...newConfig,
                            infrastructure: { ...newConfig.infrastructure, needs_file_system: e.target.checked }
                          })}
                          className="w-4 h-4 rounded bg-black border-gray-700"
                        />
                        Needs File System
                      </label>
                    </div>

                    {newConfig.infrastructure.needs_database && (
                      <select
                        value={newConfig.infrastructure.database_type}
                        onChange={(e) => setNewConfig({
                          ...newConfig,
                          infrastructure: { ...newConfig.infrastructure, database_type: e.target.value }
                        })}
                        className="w-full px-4 py-3 bg-black/50 border border-gray-800 rounded-xl text-white"
                      >
                        <option value="mysql">MySQL</option>
                        <option value="postgres">PostgreSQL</option>
                        <option value="sqlite">SQLite</option>
                      </select>
                    )}

                    <input
                      type="text"
                      placeholder="Base Image (e.g., php:8.0-apache)"
                      value={newConfig.infrastructure.docker_requirements.base_image}
                      onChange={(e) => setNewConfig({
                        ...newConfig,
                        infrastructure: {
                          ...newConfig.infrastructure,
                          docker_requirements: {
                            ...newConfig.infrastructure.docker_requirements,
                            base_image: e.target.value
                          }
                        }
                      })}
                      className="w-full px-4 py-3 bg-black/50 border border-gray-800 rounded-xl text-white focus:outline-none focus:border-orange-500"
                    />

                    <div>
                      <label className="block text-sm text-gray-400 mb-2">Extensions (comma-separated)</label>
                      <input
                        type="text"
                        placeholder="e.g., mysqli, pdo, pdo_mysql"
                        value={newConfig.infrastructure.docker_requirements.extensions.join(', ')}
                        onChange={(e) => setNewConfig({
                          ...newConfig,
                          infrastructure: {
                            ...newConfig.infrastructure,
                            docker_requirements: {
                              ...newConfig.infrastructure.docker_requirements,
                              extensions: e.target.value.split(',').map(s => s.trim()).filter(Boolean)
                            }
                          }
                        })}
                        className="w-full px-4 py-3 bg-black/50 border border-gray-800 rounded-xl text-white focus:outline-none focus:border-orange-500"
                      />
                    </div>

                    <div>
                      <label className="block text-sm text-gray-400 mb-2">Packages (comma-separated)</label>
                      <input
                        type="text"
                        placeholder="e.g., curl, vim, net-tools"
                        value={newConfig.infrastructure.docker_requirements.packages.join(', ')}
                        onChange={(e) => setNewConfig({
                          ...newConfig,
                          infrastructure: {
                            ...newConfig.infrastructure,
                            docker_requirements: {
                              ...newConfig.infrastructure.docker_requirements,
                              packages: e.target.value.split(',').map(s => s.trim()).filter(Boolean)
                            }
                          }
                        })}
                        className="w-full px-4 py-3 bg-black/50 border border-gray-800 rounded-xl text-white focus:outline-none focus:border-orange-500"
                      />
                    </div>
                  </div>
                )}
              </div>

              {/* DATABASE SCHEMA */}
              {newConfig.infrastructure.needs_database && (
                <div className="border border-gray-800 rounded-xl p-6 bg-black/30">
                  <button
                    type="button"
                    onClick={() => toggleSection('database')}
                    className="w-full flex items-center justify-between mb-4"
                  >
                    <h3 className="text-xl font-bold flex items-center gap-2">
                      <Database className="w-5 h-5 text-orange-500" />
                      Database Schema
                    </h3>
                    {expandedSections.database ? <ChevronUp /> : <ChevronDown />}
                  </button>

                  {expandedSections.database && (
                    <div className="space-y-4">
                      <input
                        type="text"
                        placeholder="Flag Location (e.g., secrets.flag)"
                        value={newConfig.database_schema.flag_location}
                        onChange={(e) => setNewConfig({
                          ...newConfig,
                          database_schema: { ...newConfig.database_schema, flag_location: e.target.value }
                        })}
                        className="w-full px-4 py-3 bg-black/50 border border-gray-800 rounded-xl text-white focus:outline-none focus:border-orange-500"
                      />

                      {/* Tables */}
                      <div>
                        <div className="flex items-center justify-between mb-3">
                          <label className="block text-sm font-medium text-gray-400">Tables</label>
                          <button
                            type="button"
                            onClick={addTable}
                            className="px-3 py-1.5 bg-gray-800 hover:bg-gray-700 text-white rounded-lg text-sm flex items-center gap-2"
                          >
                            <Plus className="w-4 h-4" />
                            Add Table
                          </button>
                        </div>
                        
                        {newConfig.database_schema.tables.map((table, tableIndex) => (
                          <div key={tableIndex} className="border border-gray-700 rounded-lg p-4 mb-3 bg-black/20">
                            <div className="flex items-center justify-between mb-3">
                              <input
                                type="text"
                                placeholder="Table name (e.g., users)"
                                value={table.name}
                                onChange={(e) => updateTable(tableIndex, 'name', e.target.value)}
                                className="flex-1 px-3 py-2 bg-black/50 border border-gray-800 rounded-lg text-white text-sm font-bold"
                              />
                              <button
                                type="button"
                                onClick={() => removeTable(tableIndex)}
                                className="ml-2 px-3 py-2 bg-red-600/20 hover:bg-red-600/30 text-red-400 rounded-lg"
                              >
                                <Trash2 className="w-4 h-4" />
                              </button>
                            </div>

                            <div className="space-y-2">
                              <label className="block text-xs text-gray-500 mb-1">Columns</label>
                              {table.columns.map((col, colIndex) => (
                                <div key={colIndex} className="flex gap-2">
                                  <input
                                    type="text"
                                    placeholder="Column definition (e.g., id INT PRIMARY KEY AUTO_INCREMENT)"
                                    value={col}
                                    onChange={(e) => updateTableColumn(tableIndex, colIndex, e.target.value)}
                                    className="flex-1 px-3 py-2 bg-black/50 border border-gray-800 rounded-lg text-white text-sm font-mono"
                                  />
                                  <button
                                    type="button"
                                    onClick={() => removeTableColumn(tableIndex, colIndex)}
                                    className="px-3 py-2 bg-red-600/20 hover:bg-red-600/30 text-red-400 rounded-lg"
                                  >
                                    <X className="w-4 h-4" />
                                  </button>
                                </div>
                              ))}
                              <button
                                type="button"
                                onClick={() => addTableColumn(tableIndex)}
                                className="px-3 py-2 bg-gray-800 hover:bg-gray-700 text-white rounded-lg text-sm flex items-center gap-2"
                              >
                                <Plus className="w-4 h-4" />
                                Add Column
                              </button>
                            </div>
                          </div>
                        ))}
                      </div>
                    </div>
                  )}
                </div>
              )}

              {/* VARIANTS */}
              <div className="border border-gray-800 rounded-xl p-6 bg-black/30">
                <button
                  type="button"
                  onClick={() => toggleSection('variants')}
                  className="w-full flex items-center justify-between mb-4"
                >
                  <h3 className="text-xl font-bold flex items-center gap-2">
                    <Sparkles className="w-5 h-5 text-orange-500" />
                    Variants
                  </h3>
                  {expandedSections.variants ? <ChevronUp /> : <ChevronDown />}
                </button>

                {expandedSections.variants && (
                  <div className="space-y-4">
                    {newConfig.variants.map((variant, index) => (
                      <div key={index} className="border border-gray-700 rounded-lg p-4 bg-black/20">
                        <div className="flex justify-between mb-3">
                          <h4 className="font-bold text-sm text-orange-400">Variant #{index + 1}</h4>
                          <button
                            type="button"
                            onClick={() => removeVariant(index)}
                            className="text-red-400 hover:text-red-300"
                          >
                            <Trash2 className="w-4 h-4" />
                          </button>
                        </div>
                        <div className="space-y-3">
                          <input
                            type="text"
                            placeholder="Variant name (e.g., Error-based SQL Injection)"
                            value={variant.name}
                            onChange={(e) => updateVariant(index, 'name', e.target.value)}
                            className="w-full px-3 py-2 bg-black/50 border border-gray-800 rounded-lg text-white text-sm"
                          />
                          <textarea
                            rows="2"
                            placeholder="Description"
                            value={variant.description}
                            onChange={(e) => updateVariant(index, 'description', e.target.value)}
                            className="w-full px-3 py-2 bg-black/50 border border-gray-800 rounded-lg text-white text-sm"
                          />
                          <input
                            type="text"
                            placeholder="Exploit example (e.g., ' OR 1=1-- -)"
                            value={variant.exploit_example}
                            onChange={(e) => updateVariant(index, 'exploit_example', e.target.value)}
                            className="w-full px-3 py-2 bg-black/50 border border-gray-800 rounded-lg text-white text-sm font-mono"
                          />
                          <div className="grid grid-cols-3 gap-2">
                            <input
                              type="number"
                              min="1"
                              max="5"
                              placeholder="Difficulty"
                              value={variant.difficulty}
                              onChange={(e) => updateVariant(index, 'difficulty', parseInt(e.target.value))}
                              className="px-3 py-2 bg-black/50 border border-gray-800 rounded-lg text-white text-sm"
                            />
                            <input
                              type="text"
                              placeholder="Sink (e.g., mysqli_query)"
                              value={variant.sink_function}
                              onChange={(e) => updateVariant(index, 'sink_function', e.target.value)}
                              className="px-3 py-2 bg-black/50 border border-gray-800 rounded-lg text-white text-sm"
                            />
                            <input
                              type="text"
                              placeholder="Output type"
                              value={variant.output_type}
                              onChange={(e) => updateVariant(index, 'output_type', e.target.value)}
                              className="px-3 py-2 bg-black/50 border border-gray-800 rounded-lg text-white text-sm"
                            />
                          </div>
                        </div>
                      </div>
                    ))}
                    <button
                      type="button"
                      onClick={addVariant}
                      className="px-4 py-2 bg-gray-800 hover:bg-gray-700 text-white rounded-xl flex items-center gap-2"
                    >
                      <Plus className="w-4 h-4" />
                      Add Variant
                    </button>
                  </div>
                )}
              </div>

              {/* ENTRY POINTS */}
              <div className="border border-gray-800 rounded-xl p-6 bg-black/30">
                <button
                  type="button"
                  onClick={() => toggleSection('entryPoints')}
                  className="w-full flex items-center justify-between mb-4"
                >
                  <h3 className="text-xl font-bold flex items-center gap-2">
                    <Zap className="w-5 h-5 text-orange-500" />
                    Entry Points
                  </h3>
                  {expandedSections.entryPoints ? <ChevronUp /> : <ChevronDown />}
                </button>

                {expandedSections.entryPoints && (
                  <div className="space-y-4">
                    {newConfig.entry_points.map((ep, index) => (
                      <div key={index} className="border border-gray-700 rounded-lg p-4 bg-black/20">
                        <div className="flex justify-between mb-3">
                          <h4 className="font-bold text-sm text-orange-400">Entry Point #{index + 1}</h4>
                          <button
                            type="button"
                            onClick={() => removeEntryPoint(index)}
                            className="text-red-400 hover:text-red-300"
                          >
                            <Trash2 className="w-4 h-4" />
                          </button>
                        </div>
                        <div className="space-y-2">
                          <select
                            value={ep.type}
                            onChange={(e) => updateEntryPoint(index, 'type', e.target.value)}
                            className="w-full px-3 py-2 bg-black/50 border border-gray-800 rounded-lg text-white text-sm"
                          >
                            <option value="">Select type...</option>
                            <option value="http_get_param">HTTP GET Parameter</option>
                            <option value="http_post_param">HTTP POST Parameter</option>
                            <option value="cookie">Cookie</option>
                            <option value="header">HTTP Header</option>
                          </select>
                          <input
                            type="text"
                            placeholder="Parameter name (e.g., id, username)"
                            value={ep.parameter_name}
                            onChange={(e) => updateEntryPoint(index, 'parameter_name', e.target.value)}
                            className="w-full px-3 py-2 bg-black/50 border border-gray-800 rounded-lg text-white text-sm"
                          />
                          <input
                            type="text"
                            placeholder="Context (e.g., user_lookup, login_form)"
                            value={ep.context}
                            onChange={(e) => updateEntryPoint(index, 'context', e.target.value)}
                            className="w-full px-3 py-2 bg-black/50 border border-gray-800 rounded-lg text-white text-sm"
                          />
                        </div>
                      </div>
                    ))}
                    <button
                      type="button"
                      onClick={addEntryPoint}
                      className="px-4 py-2 bg-gray-800 hover:bg-gray-700 text-white rounded-xl flex items-center gap-2"
                    >
                      <Plus className="w-4 h-4" />
                      Add Entry Point
                    </button>
                  </div>
                )}
              </div>

              {/* MUTATION AXES */}
              <div className="border border-gray-800 rounded-xl p-6 bg-black/30">
                <button
                  type="button"
                  onClick={() => toggleSection('mutation')}
                  className="w-full flex items-center justify-between mb-4"
                >
                  <h3 className="text-xl font-bold flex items-center gap-2">
                    <Hammer className="w-5 h-5 text-orange-500" />
                    Mutation Axes
                  </h3>
                  {expandedSections.mutation ? <ChevronUp /> : <ChevronDown />}
                </button>

                {expandedSections.mutation && (
                  <div className="space-y-6">
                    {/* Filters */}
                    {['basic', 'medium', 'advanced'].map((level) => (
                      <div key={level} className="border border-gray-700 rounded-lg p-4 bg-black/10">
                        <div className="flex items-center justify-between mb-3">
                          <h4 className="font-bold text-sm capitalize text-gray-300">{level} Filters</h4>
                          <button
                            type="button"
                            onClick={() => addFilter(level)}
                            className="px-3 py-1.5 bg-gray-800 hover:bg-gray-700 text-white rounded-lg text-xs flex items-center gap-2"
                          >
                            <Plus className="w-3 h-3" />
                            Add
                          </button>
                        </div>
                        <div className="space-y-3">
                          {newConfig.mutation_axes.filters[level].map((filter, idx) => (
                            <div key={idx} className="border border-gray-700 rounded-lg p-3 bg-black/20">
                              <div className="flex justify-between mb-2">
                                <span className="text-xs text-gray-500">Filter #{idx + 1}</span>
                                <button
                                  type="button"
                                  onClick={() => removeFilter(level, idx)}
                                  className="text-red-400 hover:text-red-300"
                                >
                                  <X className="w-3 h-3" />
                                </button>
                              </div>
                              <div className="space-y-2">
                                <input
                                  type="text"
                                  placeholder="Filter name"
                                  value={filter.name}
                                  onChange={(e) => updateFilter(level, idx, 'name', e.target.value)}
                                  className="w-full px-3 py-2 bg-black/50 border border-gray-800 rounded-lg text-white text-xs"
                                />
                                <input
                                  type="text"
                                  placeholder="Type"
                                  value={filter.type}
                                  onChange={(e) => updateFilter(level, idx, 'type', e.target.value)}
                                  className="w-full px-3 py-2 bg-black/50 border border-gray-800 rounded-lg text-white text-xs"
                                />
                                <textarea
                                  rows="2"
                                  placeholder="PHP code"
                                  value={filter.php_code}
                                  onChange={(e) => updateFilter(level, idx, 'php_code', e.target.value)}
                                  className="w-full px-3 py-2 bg-black/50 border border-gray-800 rounded-lg text-white text-xs font-mono"
                                />
                                <input
                                  type="text"
                                  placeholder="Bypass hint"
                                  value={filter.bypass_hint}
                                  onChange={(e) => updateFilter(level, idx, 'bypass_hint', e.target.value)}
                                  className="w-full px-3 py-2 bg-black/50 border border-gray-800 rounded-lg text-white text-xs"
                                />
                              </div>
                            </div>
                          ))}
                        </div>
                      </div>
                    ))}

                    {/* Contexts */}
                    <div className="border border-gray-700 rounded-lg p-4 bg-black/10">
                      <div className="flex items-center justify-between mb-3">
                        <h4 className="font-bold text-sm text-gray-300">Contexts</h4>
                        <button
                          type="button"
                          onClick={addContext}
                          className="px-3 py-1.5 bg-gray-800 hover:bg-gray-700 text-white rounded-lg text-xs flex items-center gap-2"
                        >
                          <Plus className="w-3 h-3" />
                          Add
                        </button>
                      </div>
                      <div className="space-y-3">
                        {newConfig.mutation_axes.contexts.map((context, idx) => (
                          <div key={idx} className="border border-gray-700 rounded-lg p-3 bg-black/20">
                            <div className="flex justify-between mb-2">
                              <span className="text-xs text-gray-500">Context #{idx + 1}</span>
                              <button
                                type="button"
                                onClick={() => removeContext(idx)}
                                className="text-red-400 hover:text-red-300"
                              >
                                <X className="w-3 h-3" />
                              </button>
                            </div>
                            <div className="space-y-2">
                              <input
                                type="text"
                                placeholder="Context name (e.g., login_form)"
                                value={context.name}
                                onChange={(e) => updateContext(idx, 'name', e.target.value)}
                                className="w-full px-3 py-2 bg-black/50 border border-gray-800 rounded-lg text-white text-xs"
                              />
                              <textarea
                                rows="2"
                                placeholder="Query template (e.g., SELECT * FROM users WHERE username='{{INPUT}}')"
                                value={context.query_template}
                                onChange={(e) => updateContext(idx, 'query_template', e.target.value)}
                                className="w-full px-3 py-2 bg-black/50 border border-gray-800 rounded-lg text-white text-xs font-mono"
                              />
                              <input
                                type="text"
                                placeholder="UI theme"
                                value={context.ui_theme}
                                onChange={(e) => updateContext(idx, 'ui_theme', e.target.value)}
                                className="w-full px-3 py-2 bg-black/50 border border-gray-800 rounded-lg text-white text-xs"
                              />
                              <input
                                type="text"
                                placeholder="Description"
                                value={context.description}
                                onChange={(e) => updateContext(idx, 'description', e.target.value)}
                                className="w-full px-3 py-2 bg-black/50 border border-gray-800 rounded-lg text-white text-xs"
                              />
                            </div>
                          </div>
                        ))}
                      </div>
                    </div>

                    {/* Sinks */}
                    <div className="border border-gray-700 rounded-lg p-4 bg-black/10">
                      <div className="flex items-center justify-between mb-3">
                        <h4 className="font-bold text-sm text-gray-300">Sinks</h4>
                        <button
                          type="button"
                          onClick={addSink}
                          className="px-3 py-1.5 bg-gray-800 hover:bg-gray-700 text-white rounded-lg text-xs flex items-center gap-2"
                        >
                          <Plus className="w-3 h-3" />
                          Add
                        </button>
                      </div>
                      <div className="space-y-2">
                        {newConfig.mutation_axes.sinks.map((sink, idx) => (
                          <div key={idx} className="flex gap-2">
                            <input
                              type="text"
                              placeholder="Sink function (e.g., mysqli_query)"
                              value={sink}
                              onChange={(e) => updateSink(idx, e.target.value)}
                              className="flex-1 px-3 py-2 bg-black/50 border border-gray-800 rounded-lg text-white text-xs font-mono"
                            />
                            <button
                              type="button"
                              onClick={() => removeSink(idx)}
                              className="px-3 py-2 bg-red-600/20 hover:bg-red-600/30 text-red-400 rounded-lg"
                            >
                              <X className="w-4 h-4" />
                            </button>
                          </div>
                        ))}
                      </div>
                    </div>
                  </div>
                )}
              </div>

              {/* AI GENERATION HINTS */}
              <div className="border border-gray-800 rounded-xl p-6 bg-black/30">
                <button
                  type="button"
                  onClick={() => toggleSection('aiHints')}
                  className="w-full flex items-center justify-between mb-4"
                >
                  <h3 className="text-xl font-bold flex items-center gap-2">
                    <Sparkles className="w-5 h-5 text-orange-500" />
                    AI Generation Hints
                  </h3>
                  {expandedSections.aiHints ? <ChevronUp /> : <ChevronDown />}
                </button>

                {expandedSections.aiHints && (
                  <div className="space-y-3">
                    <textarea
                      rows="2"
                      placeholder="Code structure hints"
                      value={newConfig.ai_generation_hints.code_structure}
                      onChange={(e) => setNewConfig({
                        ...newConfig,
                        ai_generation_hints: { ...newConfig.ai_generation_hints, code_structure: e.target.value }
                      })}
                      className="w-full px-4 py-3 bg-black/50 border border-gray-800 rounded-xl text-white text-sm focus:outline-none focus:border-orange-500"
                    />
                    <input
                      type="text"
                      placeholder="Database connection string"
                      value={newConfig.ai_generation_hints.database_connection}
                      onChange={(e) => setNewConfig({
                        ...newConfig,
                        ai_generation_hints: { ...newConfig.ai_generation_hints, database_connection: e.target.value }
                      })}
                      className="w-full px-4 py-3 bg-black/50 border border-gray-800 rounded-xl text-white text-sm focus:outline-none focus:border-orange-500"
                    />
                    <textarea
                      rows="2"
                      placeholder="Vulnerability placement hints"
                      value={newConfig.ai_generation_hints.vulnerability_placement}
                      onChange={(e) => setNewConfig({
                        ...newConfig,
                        ai_generation_hints: { ...newConfig.ai_generation_hints, vulnerability_placement: e.target.value }
                      })}
                      className="w-full px-4 py-3 bg-black/50 border border-gray-800 rounded-xl text-white text-sm focus:outline-none focus:border-orange-500"
                    />
                    <input
                      type="text"
                      placeholder="Output format"
                      value={newConfig.ai_generation_hints.output_format}
                      onChange={(e) => setNewConfig({
                        ...newConfig,
                        ai_generation_hints: { ...newConfig.ai_generation_hints, output_format: e.target.value }
                      })}
                      className="w-full px-4 py-3 bg-black/50 border border-gray-800 rounded-xl text-white text-sm focus:outline-none focus:border-orange-500"
                    />
                    <input
                      type="text"
                      placeholder="Dockerfile notes"
                      value={newConfig.ai_generation_hints.dockerfile_notes}
                      onChange={(e) => setNewConfig({
                        ...newConfig,
                        ai_generation_hints: { ...newConfig.ai_generation_hints, dockerfile_notes: e.target.value }
                      })}
                      className="w-full px-4 py-3 bg-black/50 border border-gray-800 rounded-xl text-white text-sm focus:outline-none focus:border-orange-500"
                    />
                  </div>
                )}
              </div>

              {/* Submit Buttons */}
              <div className="flex gap-4 pt-4 border-t border-gray-800">
                <button
                  type="submit"
                  disabled={loading}
                  className="flex-1 px-8 py-4 bg-gradient-to-r from-orange-500 to-orange-600 hover:from-orange-600 hover:to-orange-700 disabled:from-gray-800 disabled:to-gray-800 text-white font-bold rounded-xl flex items-center justify-center gap-2 transition-all"
                >
                  {loading ? (
                    <>
                      <Loader className="w-5 h-5 animate-spin" />
                      Creating & Generating...
                    </>
                  ) : (
                    <>
                      <Rocket className="w-5 h-5" />
                      Create Config & Generate Machine
                    </>
                  )}
                </button>
                <button
                  type="button"
                  onClick={() => setShowCreateForm(false)}
                  className="px-8 py-4 bg-gray-800 hover:bg-gray-700 text-white rounded-xl transition-all"
                >
                  Cancel
                </button>
              </div>
            </form>
          </div>
        )}

        {/* Configs List */}
        <div className="rounded-2xl border border-gray-900 bg-gradient-to-br from-gray-900/50 to-black/50 backdrop-blur overflow-hidden">
          <div className="px-6 py-4 border-b border-gray-800">
            <h2 className="text-xl font-bold flex items-center gap-2">
              <Code className="w-5 h-5 text-orange-500" />
              Available Configs ({configs.length})
            </h2>
          </div>

          {configs.length === 0 ? (
            <div className="p-12 text-center">
              <Settings className="w-16 h-16 text-gray-700 mx-auto mb-4" />
              <h3 className="text-xl font-bold text-gray-600 mb-2">No Configs Found</h3>
              <p className="text-gray-500 mb-6">Create your first vulnerability config to get started</p>
              <button
                onClick={() => setShowCreateForm(true)}
                className="px-6 py-3 bg-orange-500 hover:bg-orange-600 text-white rounded-xl inline-flex items-center gap-2 transition-all"
              >
                <Plus className="w-5 h-5" />
                Create Config
              </button>
            </div>
          ) : (
            <div className="divide-y divide-gray-800">
              {configs.map((config) => (
                <div key={config.filename} className="p-6 hover:bg-gray-900/30 transition-all">
                  <div className="flex items-start justify-between">
                    <div className="flex-1">
                      <div className="flex items-center gap-3 mb-3">
                        <div className="p-2 rounded-lg bg-orange-500/20">
                          <FileCode className="w-5 h-5 text-orange-500" />
                        </div>
                        <div>
                          <h3 className="text-lg font-bold text-white">{config.name}</h3>
                          <p className="text-sm text-gray-500">
                            {config.vulnerability_id} • {config.category}
                          </p>
                        </div>
                      </div>
                      <p className="text-sm text-gray-400 mb-3">{config.description}</p>
                      <div className="flex flex-wrap gap-2">
                        <span className="px-2 py-1 bg-gray-800 text-gray-300 rounded text-xs">
                          {config.variants_count} variants
                        </span>
                        <span className="px-2 py-1 bg-gray-800 text-gray-300 rounded text-xs">
                          Difficulty {config.difficulty_range[0]}-{config.difficulty_range[1]}
                        </span>
                      </div>
                    </div>

                    <button
                      onClick={() => handleGenerateMachine(config.category)}
                      disabled={generatingMachine === config.category}
                      className="px-4 py-2 bg-orange-600/20 hover:bg-orange-600/30 disabled:bg-gray-800 text-orange-400 disabled:text-gray-600 rounded-xl flex items-center gap-2 transition-all"
                    >
                      {generatingMachine === config.category ? (
                        <>
                          <Loader className="w-4 h-4 animate-spin" />
                          Generating...
                        </>
                      ) : (
                        <>
                          <Rocket className="w-4 h-4" />
                          Generate Machine
                        </>
                      )}
                    </button>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default ConfigManager;
