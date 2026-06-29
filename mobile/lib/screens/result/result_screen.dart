import 'package:flutter/material.dart';
import 'package:mobile/services/api_service.dart';
import 'package:mobile/models/response.dart';

class ResultScreen extends StatefulWidget {
  final String requestId;

  const ResultScreen({super.key, required this.requestId});

  @override
  State<ResultScreen> createState() => _ResultScreenState();
}

class _ResultScreenState extends State<ResultScreen> {
  final ApiService _apiService = ApiService();
  late Future<TriageResult> _resultFuture;

  @override
  void initState() {
    super.initState();
    _resultFuture = _apiService.getResult(widget.requestId);
  }

  String _formatAgentName(String name) {
    final normalized = name.replaceAll('_', '').toLowerCase();
    
    const Map<String, String> displayNames = {
      'validation': 'Validation',
      'ocr': 'OCR',
      'piidetection': 'PII Detection',
      'piisanitization': 'PII Sanitization',
      'intentclassification': 'Intent Classification',
      'medicalcomplexity': 'Medical Complexity',
      'urgencyassignment': 'Urgency Assignment',
      'router': 'Router',
      'medicalreasoning': 'Medical Reasoning',
      'localknowledge': 'Local Knowledge',
      'formatter': 'Formatter',
      'auditlogger': 'Audit Logger',
    };

    if (displayNames.containsKey(normalized)) {
      return displayNames[normalized]!;
    }

    return name.split('_').map((word) {
      if (word.isEmpty) return word;
      return word[0].toUpperCase() + word.substring(1).toLowerCase();
    }).join(' ');
  }

  String _formatDuration(int ms) {
    if (ms >= 1000) {
      return '${(ms / 1000).toStringAsFixed(1)} s';
    }
    return '$ms ms';
  }

  String _formatLatency(double ms) {
    if (ms >= 1000) {
      return '${(ms / 1000).toStringAsFixed(2)} s';
    }
    return '${ms.toInt()} ms';
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Theme.of(context).colorScheme.surface,
      appBar: AppBar(
        title: const Text('Triage Result'),
        centerTitle: true,
      ),
      body: FutureBuilder<TriageResult>(
        future: _resultFuture,
        builder: (context, snapshot) {
          if (snapshot.connectionState == ConnectionState.waiting) {
            return const Center(child: CircularProgressIndicator());
          } else if (snapshot.hasError) {
            return _buildErrorWidget(snapshot.error.toString());
          } else if (!snapshot.hasData) {
            return const Center(child: Text('No data found'));
          }

          final result = snapshot.data!;
          final isStructured = result.summary != null;

          return SingleChildScrollView(
            padding: const EdgeInsets.symmetric(horizontal: 16.0, vertical: 12.0),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.stretch,
              children: [
                if (isStructured) ...[
                  _buildMainPatientCard(result),
                  const SizedBox(height: 16),
                  _buildSectionHeader('Clinical Summary'),
                  _buildSummaryCard(result.summary!),
                ] else ...[
                  _buildSectionHeader('Response'),
                  _buildRawResponseCard(result.rawResponse ?? 'No response received'),
                ],
                
                const SizedBox(height: 24),
                Theme(
                  data: Theme.of(context).copyWith(dividerColor: Colors.transparent),
                  child: ExpansionTile(
                    title: Text(
                      'Technical Details',
                      style: Theme.of(context).textTheme.titleSmall?.copyWith(
                            color: Colors.grey[600],
                            fontWeight: FontWeight.bold,
                          ),
                    ),
                    childrenPadding: EdgeInsets.zero,
                    tilePadding: const EdgeInsets.symmetric(horizontal: 4),
                    children: [
                      if (result.detectedEntities.isNotEmpty) ...[
                        _buildSectionHeader('Detected Entities'),
                        _buildEntitiesCard(result.detectedEntities),
                        const SizedBox(height: 12),
                      ],
                      _buildSectionHeader('Analysis Insights'),
                      _buildInsightsGrid(result),
                      const SizedBox(height: 12),
                      _buildSectionHeader('System Details'),
                      _buildDetailsCard(result),
                      const SizedBox(height: 12),
                      _buildSectionHeader('Execution Timeline'),
                      _buildExecutionPathCard(result.executionPath),
                    ],
                  ),
                ),
                
                const SizedBox(height: 32),
                FilledButton(
                  onPressed: () => Navigator.of(context).popUntil((route) => route.isFirst),
                  style: FilledButton.styleFrom(
                    padding: const EdgeInsets.symmetric(vertical: 16),
                    shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
                  ),
                  child: const Text('Start New Triage'),
                ),
                const SizedBox(height: 32),
              ],
            ),
          );
        },
      ),
    );
  }

  Widget _buildErrorWidget(String error) {
    return Center(
      child: Padding(
        padding: const EdgeInsets.all(24.0),
        child: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            const Icon(Icons.error_outline, color: Colors.red, size: 48),
            const SizedBox(height: 16),
            Text('Error: $error', textAlign: TextAlign.center),
            const SizedBox(height: 24),
            ElevatedButton(
              onPressed: () => setState(() {
                _resultFuture = _apiService.getResult(widget.requestId);
              }),
              child: const Text('Retry'),
            )
          ],
        ),
      ),
    );
  }

  Widget _buildMainPatientCard(TriageResult result) {
    Color riskColor;
    IconData riskIcon;
    switch (result.riskLevel?.toUpperCase()) {
      case 'HIGH':
        riskColor = Colors.red;
        riskIcon = Icons.warning_rounded;
        break;
      case 'MEDIUM':
        riskColor = Colors.orange;
        riskIcon = Icons.info_rounded;
        break;
      case 'LOW':
        riskColor = Colors.green;
        riskIcon = Icons.check_circle_rounded;
        break;
      default:
        riskColor = Colors.blue;
        riskIcon = Icons.help_outline_rounded;
    }

    return Card(
      elevation: 0,
      color: riskColor.withValues(alpha: 0.08),
      shape: RoundedRectangleBorder(
        borderRadius: BorderRadius.circular(20),
        side: BorderSide(color: riskColor.withValues(alpha: 0.2), width: 1.5),
      ),
      child: Padding(
        padding: const EdgeInsets.all(20.0),
        child: Column(
          children: [
            Row(
              children: [
                Icon(riskIcon, color: riskColor, size: 36),
                const SizedBox(width: 16),
                Expanded(
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Text(
                        'Result: ${result.riskLevel} Risk',
                        style: TextStyle(
                          color: riskColor,
                          fontWeight: FontWeight.bold,
                          fontSize: 22,
                        ),
                      ),
                      Text(
                        'Urgency: ${result.urgency.toUpperCase()}',
                        style: TextStyle(
                          fontSize: 13, 
                          fontWeight: FontWeight.w500, 
                          color: riskColor.withValues(alpha: 0.8)
                        ),
                      ),
                    ],
                  ),
                ),
              ],
            ),
            const Padding(
              padding: EdgeInsets.symmetric(vertical: 16.0),
              child: Divider(),
            ),
            Row(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Icon(Icons.medical_services, color: Theme.of(context).colorScheme.primary, size: 24),
                const SizedBox(width: 16),
                Expanded(
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Text(
                        'NEXT STEP',
                        style: TextStyle(
                          fontSize: 11,
                          letterSpacing: 1,
                          fontWeight: FontWeight.bold,
                          color: Colors.grey[700],
                        ),
                      ),
                      const SizedBox(height: 4),
                      Text(
                        result.recommendedNextStep!,
                        style: Theme.of(context).textTheme.titleMedium?.copyWith(
                              fontWeight: FontWeight.bold,
                              height: 1.3,
                            ),
                      ),
                    ],
                  ),
                ),
              ],
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildSectionHeader(String title) {
    return Padding(
      padding: const EdgeInsets.only(left: 4, bottom: 8, top: 8),
      child: Text(
        title.toUpperCase(),
        style: Theme.of(context).textTheme.labelSmall?.copyWith(
              color: Colors.grey[600],
              fontWeight: FontWeight.bold,
              letterSpacing: 1.1,
            ),
      ),
    );
  }

  Widget _buildSummaryCard(String summary) {
    return Container(
      padding: const EdgeInsets.all(16),
      decoration: BoxDecoration(
        color: Theme.of(context).colorScheme.surfaceContainerHigh,
        borderRadius: BorderRadius.circular(16),
      ),
      child: Text(
        summary,
        style: Theme.of(context).textTheme.bodyMedium?.copyWith(height: 1.5),
      ),
    );
  }

  Widget _buildRawResponseCard(String response) {
    return Container(
      padding: const EdgeInsets.all(20),
      decoration: BoxDecoration(
        color: Theme.of(context).colorScheme.primaryContainer.withValues(alpha: 0.3),
        borderRadius: BorderRadius.circular(20),
        border: Border.all(color: Theme.of(context).colorScheme.primary.withValues(alpha: 0.2)),
      ),
      child: Text(
        response,
        style: Theme.of(context).textTheme.bodyLarge?.copyWith(height: 1.6),
      ),
    );
  }

  Widget _buildEntitiesCard(List<String> entities) {
    return Wrap(
      spacing: 8,
      runSpacing: 4,
      children: entities.map((entity) => Chip(
        label: Text(entity, style: const TextStyle(fontSize: 11)),
        padding: EdgeInsets.zero,
        visualDensity: VisualDensity.compact,
        backgroundColor: Theme.of(context).colorScheme.surfaceContainerHigh,
        side: BorderSide.none,
        shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(8)),
      )).toList(),
    );
  }

  Widget _buildInsightsGrid(TriageResult result) {
    return GridView.count(
      shrinkWrap: true,
      physics: const NeverScrollableScrollPhysics(),
      crossAxisCount: 2,
      mainAxisSpacing: 8,
      crossAxisSpacing: 8,
      childAspectRatio: 2.5,
      children: [
        _buildInsightItem(Icons.psychology_alt, 'Intent', result.intent),
        _buildInsightItem(Icons.speed, 'Urgency', result.urgency),
        _buildInsightItem(Icons.layers, 'Complexity', result.complexity.toStringAsFixed(1)),
        _buildInsightItem(Icons.security, 'PII Status', result.containsPii ? 'Yes' : 'No'),
      ],
    );
  }

  Widget _buildInsightItem(IconData icon, String label, String value) {
    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 6),
      decoration: BoxDecoration(
        color: Theme.of(context).colorScheme.surfaceContainerHighest.withValues(alpha: 0.3),
        borderRadius: BorderRadius.circular(10),
      ),
      child: Row(
        children: [
          Icon(icon, size: 16, color: Colors.grey[700]),
          const SizedBox(width: 8),
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                Text(label, style: const TextStyle(fontSize: 9, color: Colors.grey)),
                Text(
                  value.toUpperCase(),
                  style: const TextStyle(fontSize: 11, fontWeight: FontWeight.bold),
                  overflow: TextOverflow.ellipsis,
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildDetailsCard(TriageResult result) {
    return Container(
      padding: const EdgeInsets.all(12),
      decoration: BoxDecoration(
        color: Theme.of(context).colorScheme.surfaceContainerHighest.withValues(alpha: 0.3),
        borderRadius: BorderRadius.circular(12),
      ),
      child: Column(
        children: [
          _buildCompactDetailRow(Icons.route, 'Route', _formatAgentName(result.route)),
          _buildCompactDetailRow(Icons.smart_toy_outlined, 'Model', result.modelUsed),
          _buildCompactDetailRow(Icons.timer_outlined, 'Latency', _formatLatency(result.latencyMs)),
        ],
      ),
    );
  }

  Widget _buildCompactDetailRow(IconData icon, String label, String value) {
    return Padding(
      padding: const EdgeInsets.symmetric(vertical: 4),
      child: Row(
        children: [
          Icon(icon, size: 14, color: Colors.grey),
          const SizedBox(width: 8),
          Text('$label: ', style: const TextStyle(fontSize: 11, color: Colors.grey)),
          Text(value, style: const TextStyle(fontSize: 11, fontWeight: FontWeight.bold)),
        ],
      ),
    );
  }

  Widget _buildExecutionPathCard(List<ExecutionStep> steps) {
    return Column(
      children: steps.map((step) => Padding(
        padding: const EdgeInsets.symmetric(vertical: 4, horizontal: 4),
        child: Row(
          children: [
            const Icon(Icons.check_circle, size: 14, color: Colors.green),
            const SizedBox(width: 8),
            Expanded(
              child: Text(
                _formatAgentName(step.name),
                style: const TextStyle(fontSize: 12),
              ),
            ),
            Text(
              _formatDuration(step.durationMs),
              style: const TextStyle(fontSize: 11, color: Colors.grey),
            ),
          ],
        ),
      )).toList(),
    );
  }
}
